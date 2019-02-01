# Spindrift

Утилита для создания легковесных Telegram-ботов из Python-функций.

## Содержание

* [Установка](#Установка)
* [Руководство](#Руководство)
    * [0. Start, help и другие команды по умолчанию](#Start-help-и-другие-команды-по-умолчанию)
    * [1. Регистрация комманд](#1-Регистрация-комманд)
    * [2. Отправка изображений](#2-Отправка-изображений)
    * [3. Контроль выполнения функций с помощью параметров](#3-Контроль-выполнения-функций-с-помощью-параметров)
    * [4. Реагирование на нажатия кнопок](#4-Реагирование-на-нажатия-кнопок)
    * [5. Логирование событий в SQLite](#5-Логирование-событий-в-SQLite)


## Установка
[К содержанию](#Содержание)

```
git clone 
cd <cloned_repo>
pip install .
```

## Руководство
[К содержанию](#Содержание)

Подготовка:
```
from spindrift.bot import TelegramBot
from spindrift.message import Message
```

### 0. Start, help и другие команды по умолчанию
[К содержанию](#Содержание)

```
bot = TelegramBot(token='<YOUR_TOKEN>')
```

Бот уже запущен и готов к работе! Давайте проверим:

```
> /start

Hello and welcome! Start using me right away or ask for /help :)

> /help

The available commands are:
→ /start: Shows the starting dialog
→ /help: Shows this message
→ /set <param> <x>: Sets parameter <param> to value <x>. Like `/set a 4`
→ /params: Shows list of all specified parameters
```

Цель команд `/set` и `/params` - дать пользователю бота возможность управлять функциями "под капотом" бота.

Сообщения после команд `/start` и `/help`, конечно, тоже можно менять:

```
bot.starting_message = 'Custom hello message'

bot.help_message = 'Custom help message'
```

### 1. Регистрация комманд
[К содержанию](#Содержание)

Функция, которая передается в качестве команды боту __должна__ принимать словарь параметров, даже если его не использует:

```
bot = TelegramBot(token='<YOUR_TOKEN>')

def hello_world(config={}):
    return Message(text='Hello world!')

bot.register_command('hello', hello_world)
```

Вы можете сразу проверить работу новой команды:

```
> /hello

Hello, world!
```

### 2. Отправка изображений
[К содержанию](#Содержание)

У класса `Message` есть два поля для поддержки отправки изображений: `image` и `image_url`. Используйте `image`, чтобы поделиться файлом с устройства (в `image` нужно передать абсолютный путь к картинке), а для ссылок из Интернета предусмотрено поле `image_url`.

Пример:

```
bot = TelegramBot(token='<YOUR_TOKEN>')

def local_funny_meme(config={}):
    return Message(image='/Users/yourName/path/to/a/meme')

bot.register_command('local_meme', local_funny_meme)


def funny_online_meme(config={}):
    return Message(image_url='https://sun1-16.userapi.com/c849332/v849332281/1207ee/tI9a_zqqY0U.jpg')

bot.register_command('online_meme', funny_online_meme)
```

### 3. Контроль выполнения функций с помощью параметров
[К содержанию](#Содержание)


### 4. Реагирование на нажатия кнопок
[К содержанию](#Содержание)


### 5. Логирование событий в SQLite
[К содержанию](#Содержание)

