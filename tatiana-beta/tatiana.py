#!/usr/bin/python3
#coding=utf-8
#Татьяна - умная домохозяйка
#Программа для ЭВМ, выполняющаяся по команде пользователя или в режиме системной службы ОС GNU/Linux Raspbian.
#Предназначется для считывания и интерпретации электрических импульсов на физических портах GPIO микрокомпьютера Raspberry Pi 2+.
#Распространяется свободно на условиях лицензии GNU GPLv2.
#Автор: Алексей Butylkus, https://vk.com/butpub, https://www.youtube.com/user/butylkus


# ========= Импортируем модули, настраиваем их ========= #

import time
import os, sys, signal, threading
from datetime import datetime
import pymysql as MYSQL #используем более короткий синоним, ибо нех
import RPi.GPIO as GPIO
import Adafruit_DHT as dht #модуль чтения датчиков DHT: https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated
import config

version = "0.7.3-1a"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 



# ========= Настраиваем пины согласно базе данных ========= #
# ========= ВАЖНО ========= #
# При перенастройке системы её НЕОБХОДИМО перезапустить!
# Настройки нельзя переопределить на лету, они НЕ вступят в силу до перезапуска данной программы.

connection = MYSQL.connect(host=config.dbhost, database=config.dbbase, user=config.dbuser, password=config.dbpassword)
cursor = connection.cursor()

# Выходные пины (управляемые)
query = "SELECT pin FROM `pins` WHERE `direction`='output'"
cursor.execute(query)
outpins = cursor.fetchall()
for pin in outpins:
    GPIO.setup(int(pin[0]), GPIO.OUT)

# Входные пины (управляющие) - кнопки для одиночных устройств
query = "SELECT pin FROM `pins` WHERE `direction`='input'"
cursor.execute(query)
inpins = cursor.fetchall()
for pin in inpins:
    GPIO.setup(int(pin[0]), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(int(pin[0]), GPIO.FALLING, bouncetime=200)

# Входные пины (управляющие) - для блочных устройств кнопки вынесены в отдельный тип
query = "SELECT pin FROM `pins` WHERE `direction`='block'"
cursor.execute(query)
blockpins = cursor.fetchall()
for pin in blockpins:
    GPIO.setup(int(pin[0]), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(int(pin[0]), GPIO.FALLING, bouncetime=200)

# Пины PIR-сенсоров.
query = "SELECT pin FROM `pins` WHERE `direction`='pir'"
cursor.execute(query)
pirpins = cursor.fetchall()
for pin in pirpins:
    GPIO.setup(int(pin[0]), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(int(pin[0]), GPIO.FALLING, bouncetime=10000)


cursor.close()
connection.close()


# Инициализируем отсечки времени. Понадобятся для главного цикла
this_moment = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") #общая
dht_moment = 0 #для датчиков температуры-влажности
plan_moment = round(time.time()) #для планировщика

global stopsignal
global capture_online
stopsignal = False
capture_online = False





# ========= Главные функции ========= #

### Проверяет и включает-выключает устройства согласно записям в БД
def device(cursor, logfile=config.logpath):
    query = "SELECT pin, status FROM `pins` WHERE `direction`='output'"
    cursor.execute(query)
    string = cursor.fetchall()
    for pairs in string:
        GPIO.output(int(pairs[0]), pairs[1])



### Обработчик плана. Обновляет статусы при наступлении запланированного момента
def check_plan(cursor, logfile=config.logpath):
    query = "SELECT pin, ontime, offtime, calendar FROM `plan`"
    cursor.execute(query)
    planarray = cursor.fetchall()
    ThisMoment = datetime.strftime(datetime.now(), "%H:%M:%S")
    for moment in planarray:
        
#Проверяем календарь: 1 = только по будням, 2 = только по выходным, 3 = ежедневно
        operable = False
        if moment[3] == 1 and (datetime.isoweekday(datetime.now()) <= 5):
            operable = True
        elif moment[3] == 2 and (datetime.isoweekday(datetime.now()) >= 6):
            operable = True
        elif moment[3] == 3:
            operable = True
        else:
            operable = False
        
        if operable == True:
            pin = moment[0]
            ontime = moment[1]
            offtime = moment[2]

#Если настал момент включения/выключения, то пишем в базу соответствующую пару пин-статус, а также делаем запись в логе
            f = open(logfile, "a")
            if ThisMoment == ontime:
                query = "UPDATE `pins` SET `status`=1 WHERE `pin`='" + str(pin) + "'"
                f.write("%PLANON% " + str(pin) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n")
            if ThisMoment == offtime:
                query = "UPDATE `pins` SET `status`=0 WHERE `pin`='" + str(pin) + "'"
                f.write("%PLANOFF% " + str(pin) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n")
            f.close()
            cursor.execute(query)
            connection.commit()



### Обработчик кнопок. Обновляет статус при нажатии на кнопку согласно привязкам в БД
def button(inpin, cursor=cursor, logfile=config.logpath):
    #узнаём привязанный выходной пин
    query = "SELECT outpin FROM `button_device` WHERE `inpin`='"+str(inpin)+"'"
    cursor.execute(query)
    outarray = cursor.fetchone() #Только один!
    #Узнаём текущий статус искомого выходного пина
    query = "SELECT status FROM `pins` WHERE `pin`='"+str(outarray[0])+"'"
    cursor.execute(query)
    status = cursor.fetchone()
    #Предформирование строки лога
    logquery = str(inpin) + " + " + str(outarray[0]) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n"
    if status[0] == 1:
        logquery ="%BUTTONOFF% " + logquery #Доформируем строку лога
        status = 0
    elif status[0] == 0:
        logquery ="%BUTTONON% " + logquery #Доформируем строку лога
        status = 1
    #Обновляем статус для привязанного выходного пина
    query = "UPDATE `pins` SET `status`='" + str(status) + "' WHERE `pin`='" + str(outarray[0]) + "'"
    cursor.execute(query)
    connection.commit()
    #Пишем лог
    lfile = open(logfile, "a")
    lfile.write(logquery)
    lfile.close()



### Обработчик блочных кнопок. Обновляет статусы по циклу при нажатии на кнопку согласно привязкам в БД button_block
def button_block(inpin, cursor=cursor, logfile=config.logpath):
    status_roll=[[0,0],[0,1],[1,0],[1,1]] #ролл-список статусов
    outarray = ()
    #узнаём привязанный выходной пин
    query = "SELECT outpin FROM `button_block` WHERE `inpin`='"+str(inpin)+"'"
    cursor.execute(query)
    outarray = cursor.fetchall() #забираем все выходные пины
    outarray = accu_list(outarray) #делаем аккуратный список выходных пинов
    statuses=[]
    for pin in outarray:
        query = "SELECT status FROM `pins` WHERE `pin`='"+str(pin)+"'"
        cursor.execute(query)
        statuses.append(cursor.fetchone())
    statuses = accu_list(statuses) #делаем аккуратный список статусов
    print(statuses)
    state = status_roll.index(statuses) #номер комбинации пинов в ролл-списке
    if state == 0:
        logquery = "%BUTTONON% " + str(inpin) + " + " + str(outarray[1]) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n"
        query = "UPDATE `pins` SET `status`='1' WHERE `pin`='" + str(outarray[1]) + "';"
    elif state == 1:
        logquery = "%BUTTONON% " + str(inpin) + " + " + str(outarray[0]) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n"
        logquery = logquery + "%BUTTONOFF% " + str(inpin) + " + " + str(outarray[1]) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n"
        query = "UPDATE `pins` SET `status`='1' WHERE `pin`='" + str(outarray[0]) + "';"
        query = query + "UPDATE `pins` SET `status`='0' WHERE `pin`='" + str(outarray[1]) + "';"
    elif state == 2:
        logquery = "%BUTTONON% " + str(inpin) + " + " + str(outarray[1]) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n"
        query = "UPDATE `pins` SET `status`='1' WHERE `pin`='" + str(outarray[1]) + "';"
    else:
        logquery = "%BUTTONOFF% " + str(inpin) + " + " + str(outarray[0]) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n"
        logquery = logquery + "%BUTTONOFF% " + str(inpin) + " + " + str(outarray[1]) + " > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n"
        query = "UPDATE `pins` SET `status`='0' WHERE `pin`='" + str(outarray[0]) + "';"
        query = query + "UPDATE `pins` SET `status`='0' WHERE `pin`='" + str(outarray[1]) + "';"
    #Пишем лог
    lfile = open(logfile, "a")
    lfile.write(logquery)
    lfile.close()
    #и в базу
    cursor.execute(query)
    connection.commit()



### Слияние всяких списков в аккуратную линию
def accu_list(array):
    result=[]
    for element in array:
        result.append(element[0])
    return result



### Обработчик датчиков температуры-влажности
### Выполняется в отдельном потоке, поэтому аргументы не нужны, а подключение к базе происходит отдельно, курсор не передаётся
def dht_reader():
    logquery = ""
    connection = MYSQL.connect(host=config.dbhost, database=config.dbbase, user=config.dbuser, password=config.dbpassword)
    cursor = connection.cursor()
    #забираем модели датчиков и их пины
    query = "SELECT pin,model FROM `dht_sensors`"
    cursor.execute(query)
    outarray = cursor.fetchall()
    #считываем показания каждого датчика
    for sensor in outarray:
        #трижды, да!
        i=0
        while i<3:
            humidity, temperature = dht.read_retry(sensor[1], sensor[0])
            if (humidity is not None) and (temperature is not None):
                nowtime = str(round(time.time()))
                temperature = str(temperature)
                humidity = str(humidity)
            i+=1
        #но сохраняем только последнее
        query = "INSERT INTO `dht_data`(`pin`, `temperature`, `humidity`, `timestamp`) VALUES ({0},{1},{2},{3})".format(sensor[0], temperature, humidity, nowtime)
        cursor.execute(query)
        connection.commit()
        logquery = logquery + "%DHTREAD% Опрос погоды {0} > {1}\n".format(sensor[0], str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")))
    cursor.close()
    connection.close()
    f = open(config.logpath, "a")
    f.write(logquery)
    f.close()



### Функция слежения через PIR-сенсор
def pir_reader(pir_pin, capture = False):
    global stopsignal
    global capture_online
    while not stopsignal:
        if (GPIO.event_detected(pir_pin) and (capture_online == False)):
            #тут надо записывать лог
            logquery = "%PIRALARM% Движение {1} > {0}\n".format(str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")), pir_pin)
            print(logquery)
            f = open(config.logpath, "a")
            f.write(logquery)
            f.close()
            if (capture == True):
                threading.Thread(target=camera_capture).start()
        time.sleep(0.1)



### Глаза Татьяны. Включает камеру и записывает заданное количество секунд.
def camera_capture():
    global capture_online
    capture_online = True
    nowtime = str(round(time.time()))
    
#################################################################
############Здесь должен быть перехват через SimpleCV############
#################################################################

    connection = MYSQL.connect(host=config.dbhost, database=config.dbbase, user=config.dbuser, password=config.dbpassword)
    cursor = connection.cursor()
    query = "INSERT INTO `pir_data`(`message`,`timestamp`) VALUES ('{0}','{1}')".format("file.avi", nowtime)
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    time.sleep(5)                                   #ВРЕМЯ ЗАПИСИ!
    capture_online = False



### Выключатель демона
def stop(signum, frame, logfile=config.logpath):
    global stopsignal
    stopsignal = True
    GPIO.cleanup() 
    f = open(logfile, "a")
    f.write("%DOWN% > " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n")
    f.close()
    sys.exit("Демон остановлен. Получен сигнал SIGTERM")







# ========= Главная программа ========= #

# Пишем в лог время старта скрипта
f = open(config.logpath, "a")
f.write("%UP% > " + str(this_moment) + "\n")
f.close()


# Инициализируем перехватчик системных сигналов для выхода из программы
signal.signal(signal.SIGTERM, stop)

# Запуск потоков охраны
for pin in pirpins:
    threading.Thread(target=pir_reader, args=[int(pin[0]), True]).start()

# Подключаемся к БД
connection = MYSQL.connect(host=config.dbhost, database=config.dbbase, user=config.dbuser, password=config.dbpassword)
cursor = connection.cursor()


# Главный вечный цикл
while True:
# Ловим нажатие кнопок - одиночные
    for pin in inpins:
        #Если кнопка нажата
        if GPIO.event_detected(int(pin[0])):
            button(pin[0], cursor)

# Ловим нажатие кнопок - блочные
    for pin in blockpins:
        #Если кнопка нажата
        if GPIO.event_detected(int(pin[0])):
            button_block(pin[0], cursor)

# Проверяем статусы и обрабатываем их
    device(cursor, config.logpath)


# Планировщик срабатывает только один раз в секунду, больше нам и не надо.
    if plan_moment != round(time.time()):
        plan_moment = round(time.time())
        check_plan(cursor, config.logpath)


# Опрос датчиков температуры-влажности проходит отдельным потоком (может занять много времени, аж до 15 секунд)
    if ((round(time.time()) - dht_moment == config.dht_interval) or (dht_moment == 0)):
        dht_moment = round(time.time())
        threading.Thread(target=dht_reader).start()


# Спим, снижая нагрузку на сервер
    time.sleep(0.05)