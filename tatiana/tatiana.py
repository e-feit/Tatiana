#!/usr/bin/python3.4
#coding=utf-8

version = "0.5b" #ААААЛЬФАААААААААА!!!!!!!!!!!!!!!

import time
from datetime import datetime
import RPi.GPIO as GPIO
import os, sys
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #Почему-то только в этом режиме

#ВЫХОДНЫЕ контакты (управление реле)
#для моей схемы подключения модуля из 4 реле. Пример работы распиновки: http://www.youtube.com/watch?v=Ln2owTgYv9M&index=4&list=PLTejl8qzLUsQuvwGsrdSC7KPgWu7mahWn
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.output(17, 1)
GPIO.output(18, 1)
GPIO.output(22, 1)
GPIO.output(27, 1)

#ВХОДНЫЕ контакты (кнопки-выключатели)
GPIO.setup(21, GPIO.IN) #тестовая кнопка

#Базовый путь к статусам:
default_path = "/home/pi/.tatiana/"

f = open(default_path + "commonlog.txt", "a")
f.write("Татьяна проснулась: " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + " \n")
f.close()


#Считывает план и возвращает список. Вызывается по ходу выполнения в контексте "по ЭТОМУ плану" для функций plan_on/off()
def planreader(plan):
    list = []
    f = open(plan, "r")
    line = f.read()
    list = line.split("\n")
    f.close()
    return list

#print (planreader("ONplan.txt")) #debug
#print("Текущее время: ", datetime.strftime(datetime.now(), "%H:%M:%S")) #контроль времени


#Функция включения выключения по планам.
#Принимает управляемый пин (устройство), план включения и план выключения.
def plan_switch(pin_out, onplan, offplan, logfile=default_path + "commonlog.txt"):
    pin_statusfile = default_path + "status/"+str(pin_out)
    try:
        f = open(pin_statusfile, "r")
        f.close()
    except FileNotFoundError:
        f = open(pin_statusfile, "w")
        status = f.write("0")
        f.close()
        status="1"
    for moment in planreader(onplan): #Вызывает считыватель плана
        if moment == datetime.strftime(datetime.now(), "%H:%M:%S"):
            #GPIO.output(pin_out,0) #Прямое включение. Конечный вариант - запись правильного статуса в правильный файл.
            #Запись в статус-файл, из него значение уйдёт на управляющую функцию device()
            f = open(pin_statusfile, "w")
            f.write("0")
            f.close()
            #print("Включено в ", moment) #при ручном запуске лучше раскомментировать, чтобы не смотреть в логи
            #Пишем в лог
            f = open(logfile, "a")
            f.write("Отметка плана для " + str(pin_out) + ", включение: " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n")
            f.close()
            while moment == datetime.strftime(datetime.now(), "%H:%M:%S"):
                continue
    for moment in planreader(offplan): #Дадада, я псих, рекурсия в наличии. Вызывает считыватель плана ещё раз на всякий пожарный
        if moment == datetime.strftime(datetime.now(), "%H:%M:%S"):
            #GPIO.output(pin_out,0) #Прямое включение. Конечный вариант - запись правильного статуса в правильный файл.
            #Запись в статус-файл, из него значение уйдёт на управляющую функцию device()
            f = open(pin_statusfile, "w")
            f.write("1")
            f.close()
            #print("Включено в ", moment) #при ручном запуске лучше раскомментировать, чтобы не смотреть в логи
            #Пишем в лог
            f = open(logfile, "a")
            f.write("Отметка плана для " + str(pin_out) + ", выключение: " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n")
            f.close()
            while moment == datetime.strftime(datetime.now(), "%H:%M:%S"):
                continue
    device(pin_out,logfile)



#Главная функция. Включает и отключает согласно статусу из соответствующего пину файла
def device(pin, logfile=default_path + "commonlog.txt"):
    f_reader = default_path + "status/"+str(pin) #Цепляем правильный файл
    f = open(f_reader,"r") #читаем статус-файл пина
    status = int(f.read())
    GPIO.output(pin, status) #Выключаем/выключаем устройство
    f.close()


#Детектор кнопок
#Принимает пин кнопки и передаёт на реле инвертированный статус по логике:
#Если кнопка нажата и реле выключено, то включить. Если нажата и реле включено - отключить
def button(pin_in, pin_out, logfile=default_path + "commonlog.txt"):
    if GPIO.input(pin_in) == False:
        #Логируем нажатие
        f = ""
        f = open(logfile, "a")
        f.write("Кнопка на пине " + str(pin_in) + " нажата " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n")
        f.close()
        #Сверяем и переключаем статус выходного устройства
        path = default_path + "status/"+str(pin_out)
        try:
            f = open(path, "r")
            status = f.read()
            f.close()
        except FileNotFoundError:
            f = open(path, "w")
            status = f.write("0")
            f.close()
            status="0"
        else:
            f = open(path, "r")
            status = f.read()
            f.close()
        #print (status) #Дебаг, отлов нажатия
        f = open(path, "w")
        stfile = open(logfile, "a")
        if status == "0":
            f.write("1")
            stfile.write("Устройство " + str(pin_out) + " выключено в " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n")
        if status == "1":
            f.write("0")
            stfile.write("Устройство " + str(pin_out) + " включено в " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + "\n")
        stfile.close()
        f.close()
        device(pin_out)
        moment = datetime.strftime(datetime.now(), "%H:%M:%S")
        while moment == datetime.strftime(datetime.now(), "%H:%M:%S"):
            continue


# ------------- ГЛАВНЫЙ ЦИКЛ ----------------

while True:
    time.sleep(0.1) #Слегка снижает нагрузку на процессор, сокращая активность до 9-10 проходов в секунду
    
    
    
    plan_switch(18, default_path + "plans/18onplan.txt", default_path + "plans/18offplan.txt", logfile=default_path + "commonlog.txt")
    plan_switch(17, default_path + "plans/17onplan.txt", default_path + "plans/17offplan.txt", logfile=default_path + "commonlog.txt")
    button(21, 27, default_path + "commonlog.txt") #По сигналу 21 пина управляется устройство на 27


# -------------  /////// ГЛАВНЫЙ ЦИКЛ ----------------


#Прибираемся при перезагрузке/рестарте
GPIO.cleanup() 
f = open(default_path + "commonlog.txt", "a")
f.write("Татьяна засыпает: " + str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")) + " \n")
f.close()
sys.exit()