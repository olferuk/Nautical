# Spindrift

The tool to make lightweight Telegram bots from plain Python functions

🇷🇺 [Здесь](#README_ru.md) есть русскоязычная версия этого README.

## Table of contents

* [Installation](#Installation)
* [Tutorial](#Tutorial)
  * [0. Start, help and other default commands](#0-Start-help-and-other-default-commands)
  * [1. Command registering](#1-Command-registering)
  * [2. Sending images](#2-Sending-images)
  * [3. Receiving images sent by user](#3-Receiving-images-sent-by-user)
  * [4. Controlling the execution with parameters](#4-Controlling-the-execution-with-parameters)
  * [5. Reacting to buttons pressed](#5-Reacting-to-buttons-pressed)
  * [6. Logging events to SQLite](#6-Logging-events-to-SQLite)
* [Contributors](#Contributors)

## Installation
[Up](#Table-of-contents)

```python
git clone https://github.com/EnlightenedCSF/Spindrift.git
cd <cloned_repo>
pip install .
```

## Tutorial
[Up](#Table-of-contents)

Preparation:
```python
from spindrift.bot import TelegramBot
from spindrift.message import Message
```

### 0. Start, help and other default commands
[Up](#Table-of-contents)

```python
bot = TelegramBot(token='<YOUR_TOKEN>', config_path='./config.db')
```

Bot is running and ready to listen to your commands! Let's check:

```bash
> /start

Hello and welcome! Start using me right away or ask for /help :)

> /help

The available commands are:
→ /start: Shows the starting dialog
→ /help: Shows this message
→ /set <param> <x>: Sets parameter <param> to value <x>. Like `/set a 4`
→ /params: Shows list of all specified parameters
```

The goal of having `/set` and `/params` command is to provide a way for a bot client to configure how underlying functions work.

You can customize messages you recieve after `/start` or `/help` commands:

```python
bot.starting_message = 'Custom hello message'

bot.help_message = 'Custom help message'
```

### 1. Command registering
[Up](#Table-of-contents)

```python
bot = TelegramBot(token='<YOUR_TOKEN>', config_path='./config.db')

def hello_world():
    return Message(text='Hello world!')

bot.register_command('hello', hello_world)
```

And it works like so:

```bash
> /hello

Hello, world!
```

### 2. Sending images
[Up](#Table-of-contents)

`Message` class has two fields to manage image sharing: `image` and `image_url`. Use `image` to share
a local file (provide a fullpath to the picture) and `image_url` to point to the image posted somewhere on the Internet.

Here is the example:

```python
bot = TelegramBot(token='<YOUR_TOKEN>', config_path='./config.db')

def local_funny_meme():
    return Message(image='/Users/yourName/path/to/a/meme')

bot.register_command('local_meme', local_funny_meme)


def funny_online_meme():
    return Message(image_url='https://sun1-16.userapi.com/c849332/v849332281/1207ee/tI9a_zqqY0U.jpg')

bot.register_command('online_meme', funny_online_meme)
```

### 3. Receiving images sent by user
[Up](#Table-of-contents)

Processing images is easy:

```python
bot = TelegramBot(token='<YOUR_TOKEN>', config_path='./config.db')

def process_photo(img):
  print('I got image of size {}'.format(img))

bot.register_photo_handler(process_photo)
```

Images the one receives are of type `PIL.JpegImagePlugin.JpegImageFile`.

### 4. Controlling the execution with parameters
[Up](#Table-of-contents)

To help bot clients control the execution, Spindrift offers parameters:

```python
bot = TelegramBot(token='<YOUR_TOKEN>', config_path='./config.db')

def function_to_control(config):
  x = int(config['x'])
  print('The x value is {}'.format(x))
  if x > 5:
    return Message(text='x is greater than 5')
  return Message(text='x is less than or equal to 5')

bot.register_command(function_to_control)
```

Pay attention: `function_to_control` could not take `config` as its first parameter. In that case, it won't
receive any user config. Vise versa, you only just need to specify first parameter in registering function to
start receiving user parameters.

It can be checked like this:

```bash
> /set x 2

Successfully set parameter "x" to "2"

> /test

x is less than or equal to 5

> /set x 10

Successfully set parameter "x" to "2"

> /test

x is greater than 5
```

__NB__: parameters are individual for each user, so assigning different values to the parameter with
the same name does not affect any other user's settings.

### 5. Reacting to buttons pressed
[Up](#Table-of-contents)

### 6. Logging events to SQLite
[Up](#Table-of-contents)

## Contributors
[Up](#Table-of-contents)

* Alexander Olferuk ( [vk](https://vk.com/a_olferuk) | [github](https://github.com/EnlightenedCSF) )
* Danila Paluhin ( [vk](https://vk.com/dpaluhin) | [github](https://github.com/Palushok) )
