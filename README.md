# Spindrift

The tool to make lightweight Telegram bots from plain Python functions

## Table of contents

* [Installation](#Installation)
* [Tutorial](#Tutorial)

## Installation
[Up](#Table-of-contents)

```
git clone
cd <cloned_repo>
pip install .
```

## Tutorial
[Up](#Table-of-contents)

Preparation:
```
from spindrift.bot import TelegramBot
from spindrift.message import Message
```

### 0. Start, help and other default commands
[Up](#Table-of-contents)

```
bot = TelegramBot(token='<YOUR_TOKEN>')
```

Bot is running and ready to listen to your commands! Let's check:

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

The goal of having `/set` and `/params` command is to provide a way for a bot client to configure how underlying functions work.

You can customize messages you recieve after `/start` or `/help` commands:

```
bot.starting_message = 'Custom hello message'

bot.help_message = 'Custom help message'
```

### 1. Command registering
[Up](#Table-of-contents)

The first and only requirement for any function is to get `config` dict as first argument:

```
bot = TelegramBot(token='<YOUR_TOKEN>')

def hello_world(config={}):
    return Message(text='Hello world!')

bot.register_command('hello', hello_world)
```

And it works like so:

```
> /hello

Hello, world!
```

### 2. Sending images
[Up](#Table-of-contents)

`Message` class has two fields to manage image sharing: `image` and `image_url`. Use `image` to share a local file (provide a fullpath to the picture) and `image_url` to point to the image posted somewhere on the Internet.

Here is the example:

```
bot = TelegramBot(token='<YOUR_TOKEN>')

def local_funny_meme(config={}):
    return Message(image='/Users/yourName/path/to/a/meme')

bot.register_command('local_meme', local_funny_meme)


def funny_online_meme(config={}):
    return Message(image_url='https://sun1-16.userapi.com/c849332/v849332281/1207ee/tI9a_zqqY0U.jpg')

bot.register_command('online_meme', funny_online_meme)
```

### 3. Receiving images sent by user
[Up](#Table-of-contents)

Processing images is easy:

```
bot = TelegramBot(token='<YOUR_TOKEN>')

def process_photo(img, config={}):
  print('I got image of size {}'.format(img))

bot.register_photo_handler(process_photo)
```

Images the one receives are of type `PIL.JpegImagePlugin.JpegImageFile`.

### 4. Controlling the execution with parameters
[Up](#Table-of-contents)

To help bot clients control the execution, Spindrift offers parameters:

```
bot = TelegramBot(token='<YOUR_TOKEN>')

def function_to_control(config):
  x = int(config['x'])
  print('The x value is {}'.format(x))
  if x > 5:
    return Message(text='x is greater than 5')
  return Message(text='x is less than or equal to 5')

bot.register_command(function_to_control)
```

It can be checked like this:

```
> /set x 2

Successfully set parameter "x" to "2"

> /test

x is less than or equal to 5

> /set x 10

Successfully set parameter "x" to "2"

> /test

x is greater than 5
```

__NB__: parameters are individual for each user, so assigning different values to the parameter with the same name does not affect any other user's settings.

### 5. Reacting to buttons pressed
[Up](#Table-of-contents)



### 6. Logging events to SQLite
[Up](#Table-of-contents)
