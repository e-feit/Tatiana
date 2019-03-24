# Требования
* Python 3

# Установка
Создать новый `venv` и установить необходимые зависимости.
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

# Запуск
```
# активировать venv, если еще не сделано
. venv/bin/activate

# указать перменную
export FLASK_APP=app.py

# запуск
flask run

# выйти из venv, если закончили работу
deactivate
```

# Разработка
Полезные для разработки конфиги (должны быть установлены перед запуском).
```
# активировать дебаггер
export FLASK_ENV=development

# авто обновление при изменении файлов
export FLASK_DEBUG=1
```

# Запустить тесты
Перед запуском не забыть войти в `venv`, все зависимости так же должны быть установлены 
(см. п. Установка).

Тесты запускаются командой:
```
python -m pytest app/
```

# Добавить/удалить зависимости
Опять же, не забыть войти в `venv`.
```
. venv/bin/activate
```
Для добавления новых зависимостей используем `pip`.
```
pip install Flask-Assets
```

После этого обязательно нужно обновить файл `requirements.txt`.
```
pip freeze > requirements.txt
```

Если что-то удаляем, то так же не забываем обновить `requirements.txt`.
```
pip uninstall Flask-Assets
pip freeze > requirements.txt
```