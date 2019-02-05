# Spindrift

Утилита для создания легковесных Telegram-ботов из Python-функций.

## Содержание

* [Установка](#Установка)
* [Руководство](#Руководство)
    * [0. Start, help и другие команды по умолчанию](#Start-help-и-другие-команды-по-умолчанию)
    * [1. Регистрация комманд](#1-Регистрация-комманд)
    * [2. Отправка изображений пользователю](#2-Отправка-изображений-пользователю)
    * [3. Загрузка изображений пользователем](#3-Загрузка-изображений-пользователем)
    * [4. Контроль выполнения функций с помощью параметров](#4-Контроль-выполнения-функций-с-помощью-параметров)
    * [5. Реагирование на нажатия кнопок](#5-Реагирование-на-нажатия-кнопок)
    * [6. Логирование событий в SQLite](#6-Логирование-событий-в-SQLite)


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
bot.starting_message = 'Другое приветственное сообщение'

bot.help_message = 'Другое сообщение о коммандах'
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

### 2. Отправка изображений пользователю
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

### 3. Загрузка изображений пользователем
[К содержанию](#Содержание)

Реагировать на загруженные изображения просто:

```
bot = TelegramBot(token='<YOUR_TOKEN>')


def process_photo(img, config={}):
  print('Получил изображение разрешением {}'.format(img))

bot.register_photo_handler(process_photo)
```

Изображение, которое функция `process_photo` получит на вход, имеет тип `PIL.JpegImagePlugin.JpegImageFile`.

### 4. Контроль выполнения функций с помощью параметров
[К содержанию](#Содержание)

Для того, чтобы пользователи могли контролировать бота, Spindrift предоставляет механизм параметров:

```
bot = TelegramBot(token='<YOUR_TOKEN>')

def function_to_control(config):
  x = int(config['x'])
  print('Значение x равно {}'.format(x))
  if x > 5:
    return Message(text='x больше 5')
  return Message(text='x меньше или равен 5')

bot.register_command('test', function_to_control)
```

В работоспособности можно убедиться следующим образом:

```
> /set x 2

Successfully set parameter "x" to "2"

> /test

x меньше или равен 5

> /set x 10

Successfully set parameter "x" to "2"

> /test

x больше 5
```

__NB__: набор параметров у каждого пользователя индивидуальный, и присвоение разными пользователями одной переменной никак не влияет на работоспособность бота у другого пользователя с его настройками.

### 5. Реагирование на нажатия кнопок
[К содержанию](#Содержание)


### 6. Логирование событий в SQLite
[К содержанию](#Содержание)

