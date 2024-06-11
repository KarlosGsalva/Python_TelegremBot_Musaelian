Проект: Telegram-бот с функцией календаря

Мусаэлян Карлен

KarlosGsalva

karlenmusaelian@gmail.com

docker-compose -f docker-compose.yml up --build

Требуется перенастроить:

.example_env -> .env

settings_template.py -> settings.py

Команда для запуска тестов бота:

docker-compose -f docker-compose.yml run bot pytest -s -vv

Команда для запуска тестов api:

docker-compose -f docker-compose.yml run django_admin pytest -s -vv