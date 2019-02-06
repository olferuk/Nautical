# Pebble

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
git clone https://github.com/EnlightenedCSF/Pebble.git
cd <cloned_repo>
pip install .
```

## Tutorial
[Up](#Table-of-contents)

Preparation:
```python
from pebble.bot import TelegramBot
from pebble.message import Message

bot = TelegramBot(token='<YOUR_TOKEN>', config_path='./config.db')
```

### 0. Start, help and other default commands
[Up](#Table-of-contents)

Create a bot like was shown in the snippet above. Your token can be acquired from the @bot_father in Telegram.

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
def process_photo(img):
  print('I got image of size {}'.format(img))

bot.register_photo_handler(process_photo)
```

Images the one receives are of type `PIL.JpegImagePlugin.JpegImageFile`.

### 4. Controlling the execution with parameters
[Up](#Table-of-contents)

To help bot clients control the execution, Pebble offers parameters:

```python
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

User parameters are stored in SQLite-file, name of which you can specify via `config_path` parameter.

### 5. Reacting to buttons pressed
[Up](#Table-of-contents)

You can add buttons to the message easily:

```python
def joke():
    return Message(message='A bear once met a burning car in the forest. He sat in it and burned alive.',
                   buttons=['😀 Ahahah', '😒 Meh'])

bot.register_command('joke', joke)
```

Their goal is to help tracking users' actions. This topic is going to be described in the next section.
Hovewer, setting callbacks to buttons pressing is not allowed yet. Stay tuned!

### 6. Logging events to SQLite
[Up](#Table-of-contents)

To known what bot's clients do, the one can enable logging.

#### 6.1. Simple logging


```python
bot = TelegramBot(token='<YOUR_TOKEN>', config_path='config.db', db_path='logs.db')

def hello():
  return Message('Hello world!')

def greet(config):
  return Message('Hello, {}!'.format(config['name']))


bot.register_command('hello', hello)
bot.register_command('greet', greet)

# Later in the Telegram:

> /hello

Hello, world!

> /set name Alex

Parameter "name" successfully set to "Alex"

> /greet

Hello, Alex!
```

There are two tables in `logs.db`: `user` and `record`. Every user's info will be recorded into the first one:


| __user_id__  | __user_name__ | __first_name__ | __last_name__ |
|--------------|---------------|----------------|---------------|
| 81910644     |               | Alexander      | Olferuk       |

And the `record` will contain full history:

| __user_id__ | __chat_id__ | __message_id__ | __dt__              | __message__    | __is_image__ | __meta__ | __button__ |
|-------------|-------------|----------------|---------------------|----------------|--------------|----------|------------|
| 81910644    | 81910628    | 598            | 2019-02-06 15:49:06 | /hello         | 0            |          |            |
| 81910644    | 81910628    | 600            | 2019-02-06 15:49:15 | /set name Alex | 0            |          |            |
| 81910644    | 81910628    | 602            | 2019-02-06 15:49:22 | /greet         | 0            |          |            |

#### 6.2. Using field meta

Let us imagine that the bot should tell one of a million funny jokes after it recieve `/joke` command.
You, as a programmer, are interested, which jokes were shown to a certain user. It is only necessary to
track joke's index in the collection. That's where parameter `meta` come in handy:

```python
JOKES = [...]

def show_random_joke():
  index = np.random.randint(len(JOKES))
  return Message(JOKES[index], meta=index)

bot.register_command('joke', show_random_joke)
```

Table `record`'s contents:

| __user_id__ | __chat_id__ | __message_id__ | __dt__              | __message__    | __is_image__ | __meta__ | __button__ |
|-------------|-------------|----------------|---------------------|----------------|--------------|----------|------------|
| 81910644    | 81910628    | 604            | 2019-02-06 16:18:08 | /joke          | 0            | 5        |            |
| 81910644    | 81910628    | 606            | 2019-02-06 16:18:11 | /joke          | 0            | 7        |            |
| 81910644    | 81910628    | 608            | 2019-02-06 16:18:15 | /joke          | 0            | 0        |            |

#### 6.3. Registering buttons taps

Let's go back to the example with a joke about bear:

```python
def joke():
    return Message(message='A bear once met a burning car in the forest. He sat in it and burned alive.',
                   buttons=['😀 Ahahah', '😒 Meh'])

bot.register_command('bear', joke)
```

Now the rating buttons taps are recorded:

| __user_id__ | __chat_id__ | __message_id__ | __dt__              | __message__    | __is_image__ | __meta__ | __button__ |
|-------------|-------------|----------------|---------------------|----------------|--------------|----------|------------|
| 81910644    | 81910628    | 610            | 2019-02-06 16:22:10 | /bear          |  0           |          |           |
| 81910644    | 81910628    | 610            | 2019-02-06 16:22:10 |                |  0           |          | 😒 Meh     |
| 81910644    | 81910628    | 613            | 2019-02-06 16:22:16 | /bear          |  0           |          |           |
| 81910644    | 81910628    | 613            | 2019-02-06 16:22:16 |                |  0           |          | 😀 Ahahah  |

The pair "bot's answer" and "user rating" is easily determined considering that `message_id` values are the
same in each pair.

## Contributors
[Up](#Table-of-contents)

* Alexander Olferuk ( [vk](https://vk.com/a_olferuk) | [github](https://github.com/EnlightenedCSF) )
* Danila Paluhin ( [vk](https://vk.com/dpaluhin) | [github](https://github.com/Palushok) )
