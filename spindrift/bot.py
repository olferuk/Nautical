from .logger import SQLiteLogger

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from functools import partial

import sys
import traceback


def make_text_handler(s):
    def f(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=s)
    return f

def make_handler(func, buttons_intro):
    def f(bot, update):
        msg = func()

        has_buttons = (msg.buttons is not None) and len(msg.buttons) > 0
        has_media = (msg.image is not None) or (msg.image_url is not None)
        has_text = msg.message is not None

        if has_media:
            photo = msg.image_url if msg.image_url is not None else open(msg.image, 'rb')
            if has_text:
                if msg.message_media_relation == 0:   #  CAPTION_ABOVE
                    bot.send_message(chat_id=update.message.chat_id, text=msg.message)  
                    bot.send_photo(chat_id=update.message.chat_id, photo=photo)
                else:                                 #  CAPTION_BELOW
                    bot.send_photo(chat_id=update.message.chat_id, photo=photo)
                    bot.send_message(chat_id=update.message.chat_id, text=msg.message)  
            else:
                bot.send_photo(chat_id=update.message.chat_id, photo=photo)
        else:
            bot.send_message(chat_id=update.message.chat_id, text=msg.message)
            
        if has_buttons:
            keyboard = [[InlineKeyboardButton(x, callback_data='{0}_{1}'\
                                             .format(x, 
                                                     str(update.message.message_id)))
                        for x in msg.buttons]]
            update.message.reply_text(buttons_intro, 
                                      reply_markup=InlineKeyboardMarkup(keyboard))
    return f

def make_buttons_processor(choice_confirmation_label):
    def f(bot, update):
        query = update.callback_query
        bot.edit_message_text(text=choice_confirmation_label.format(query.data.split('_')[0]),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
    return f

def make_set_command(setter, confirmation_label):
    def f(bot, update):
        key, value = update.message.text.split(' ')[1:]
        setter(key, value)
        bot.send_message(chat_id=update.message.chat_id, 
                         text=confirmation_label.format(key, value))
    return f

def make_params_command(vocab, no_params_label, params_title):
    def f(bot, update):
        if len(vocab) == 0:
            total = no_params_label
        else:
            title = params_title
            underscore = '========'
            s = '\n'.join(['{0} = {1}'.format(k,v) for k, v in vocab.items()])
            total = '\n'.join([title, underscore, s])
        bot.send_message(chat_id=update.message.chat_id, text=total)
    return f


class TelegramBot():
    def __init__(self, token, db_path=None):
        self.token = token
        
        self.logging = False
        if not (db_path is None):
            self.logger = TelegramLogger(db_path)
            self.logging = True
        
        self.parameters = {}
        self.fs = {}
        
        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher
        
        self._start_text = 'Hello and welcome! Start using me right away or ask for /help :)'
        self._help_text = ('The available commands are:\n'
                           '→ /start: Shows the starting dialog\n'
                           '→ /help: Shows this message\n'
                           '→ /set <param> <x>: Sets parameter <param> to value <x>. Like `/set a 4`\n'
                           '→ /params: Shows list of all specified parameters')
        
        # todo: rebuild callback when strings change
        self._parameters_title = 'Parameters are:'
        self._no_parameters_label = 'No parameters specified'
        self._param_changed_confirmation_label = 'The parameter "{0}" successfully set to "{1}"'
        self._button_press_invitation_label = 'Rate:'
        self._button_press_confirmation_label = 'You chose "{0}"'
        
        self._set_text_command('start', self._start_text)
        self._set_text_command('help', self._help_text)
        
        # /set
        self.dispatcher.add_handler(
            CommandHandler('set', 
                           make_set_command(self._set_param,
                                            self._param_changed_confirmation_label)
                          ))
        # /params
        self.dispatcher.add_handler(
            CommandHandler('params', 
                           make_params_command(self.parameters, 
                                               self._no_parameters_label,
                                               self._parameters_title)
                          ))
        # Buttons
        self.dispatcher.add_handler(
            CallbackQueryHandler(make_buttons_processor(self._button_press_confirmation_label)
                                ))
        self.resume()
        
    def register_command(self, name, f):
        self.fs[name] = f
        if self.command_with_name(name) is None:
            self.dispatcher.add_handler(
                CommandHandler(name, make_handler(f, self._button_press_invitation_label)))
        else:
            command = self.command_with_name(name)
            command.callback = make_handler(f, self._button_press_invitation_label)
            
    def _set_text_command(self, name, return_text):
        if len(self.dispatcher.handlers) == 0:
            self.dispatcher.add_handler(CommandHandler(name, make_text_handler(return_text)))
            return
        was_found = False
        for command in self.dispatcher.handlers[0]:
            if type(command) == CommandHandler and command.command[0] == name:
                was_found = True
                command.callback = make_text_handler(return_text)
        if not was_found:
            self.dispatcher.add_handler(CommandHandler(name, make_text_handler(return_text)))
    
    def _set_param(self, key, value):
        ps = self.parameters
        to_update = False
        if (key not in ps) or ((key in ps) and (ps[key] != value)):
            ps[key] = value
            to_update = True
        if to_update:
            for command_name, f in self.fs.items():
                command = self.command_with_name(command_name)
                command.callback = make_handler(partial(f, ps), 
                                                self._button_press_invitation_label)
        
    def command_with_name(self, name):
        for command in self.dispatcher.handlers[0]:
            if type(command) == CommandHandler and command.command[0] == name:
                return command
        return None
        
    def has_command_with_name(self, name):
        return self.command_with_name(name) is None
    
    def stop(self):
        self.updater.stop_polling()
        self.started = False
        
    def resume(self):
        self.updater.start_polling()
        self.started = True
    
    def commands(self):
        return [x.command[0] for x in self.dispatcher.handlers[0]]
    
    @property
    def starting_message():
        return self._help_text

    @starting_message.setter
    def starting_message(self, value):
        self._start_text = value
        self._set_text_command('start', self._start_text)
    
    @property
    def help_message(self):
        return self._start_text
    
    @help_message.setter
    def help_message(self, value):
        self._help_text = value
        self._set_text_command('help', self._help_text)

#         try:
#             <CODE>
#             except BaseException as ex:
#                 ex_type, ex_value, ex_traceback = sys.exc_info()
#                 trace_back = traceback.extract_tb(ex_traceback)
#                 stack_trace = [('File : %s\n'
#                                 '\tFunction: %s\n'
#                                 '\tLine: %s\n'
#                                 '\tMessage: %s)') % (t[0], t[1], t[2], t[3]) 
#                                for t in trace_back]
#                 print('{0} ({1})'.format(ex_type.__name__, ex_value))
#                 for s in stack_trace:
#                     print(s)
