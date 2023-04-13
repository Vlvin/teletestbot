import os
import var
import sqlite3
import telebot
from telebot import types
token = "TOKEN"

bot = telebot.TeleBot(token, parse_mode=None)

strmsg = ('Hello. I am TestBot\n'
          'Click "Help" if you want to know about my functions\n'
          'Click "Info" if you want to know about my creator')

infomsg = ('Hi. This is TestBot made by vlvin\n'
           'to discover abilities of PyTelegramBotApi lib\n'
           'if you want to use sourcecode\n'
           'you can find it here https://github.com/Vlvin/teletestbot\n'
           'if you have questions, please contact me @GOTV3454')

helpmsg = ('Back to the menu - returns you to Main Menu\n'
           'Help - showing this message\n'
           'Calculator - NOW user friendly evaluator\n'
           'Users - showing bot users\n'
           'Send - sending message to chosen user')
a = ""


def addd(id,fir,las):
    conn = sqlite3.connect("ID.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    cursor.execute(f"""INSERT INTO users VALUES
    (?,?,?);""", (id,f"{fir}",f"{las}"))
    conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
def fstart(message):
    addd(message.chat.id,message.from_user.first_name,message.from_user.last_name)
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.row(types.InlineKeyboardButton('Help',callback_data=f'help.{message.chat.id}'),
            types.InlineKeyboardButton('Info',callback_data=f'info.{message.chat.id}'))
    mrk.row(types.InlineKeyboardButton('Users',callback_data=f'users.{message.chat.id}'),
            types.InlineKeyboardButton('Calculator',callback_data=f'calc.{message.chat.id}'))
    var.b[message.chat.id] = bot.send_message(chat_id=message.chat.id,text=strmsg,reply_markup=mrk)


def hell(message):
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.row(types.InlineKeyboardButton('Back to menu', callback_data=f'start.{message.chat.id}'))
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.id,text=helpmsg,reply_markup=mrk)


def info(message):
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.row(types.InlineKeyboardButton('Back to menu', callback_data=f'start.{message.chat.id}'))
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.id,text=infomsg,reply_markup=mrk)


def menu(message):
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.row(types.InlineKeyboardButton('Help',callback_data=f'help.{message.chat.id}'),
            types.InlineKeyboardButton('Info',callback_data=f'info.{message.chat.id}'))
    mrk.row(types.InlineKeyboardButton('Users',callback_data=f'users.{message.chat.id}'),
            types.InlineKeyboardButton('Calculator',callback_data=f'calc.{message.chat.id}'))
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.id,
                          text=strmsg,
                          reply_markup=mrk)


def send(message):
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.row(types.InlineKeyboardButton('Menu',callback_data=f'start.{message.chat.id}'))
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.id,text=roww()+'\nEnter user id',reply_markup=mrk)
    bot.register_next_step_handler(var.b[message.chat.id],send2)


def send2(message):
    var.id[message.chat.id] = message.text
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.row(types.InlineKeyboardButton('Menu',callback_data=f'start.{message.chat.id}'))
    bot.edit_message_text(chat_id=var.b[message.chat.id].chat.id,
                          message_id=var.b[message.chat.id].id,
                          text=roww()+'\nEnter message to send',
                          reply_markup=mrk)
    bot.delete_message(chat_id=message.chat.id,message_id=message.id)
    bot.register_next_step_handler(var.b[message.chat.id],send3)


def send3(message):
    var.message[message.chat.id] = message.text
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.row(types.InlineKeyboardButton('Menu',
                                       callback_data=f'start.{message.chat.id}'))
    bot.send_message(chat_id=var.id[message.chat.id],
                     text=f'{message.from_user.first_name}: {var.message[message.chat.id]}')
    bot.edit_message_text(chat_id=var.b[message.chat.id].chat.id,
                          message_id=var.b[message.chat.id].id,
                          text=roww()+'\nMessage succesfully sent',
                          reply_markup=mrk)
    bot.delete_message(chat_id=message.chat.id,message_id=message.id)

def roww():
    row = sqlite3.connect("ID.db", check_same_thread=False).cursor().execute("SELECT * FROM users").fetchall()
    print(row)
    x = ''
    for g in row:
        x += '\n'
        for i in g:
            x += f'{i} '
    return x


def users(message):
    row = sqlite3.connect("ID.db", check_same_thread=False).cursor().execute("SELECT * FROM users").fetchall()
    print(row)
    x = ''
    for g in row:
        x += '\n'
        for i in g:
            x += f'{i} '
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.add(types.InlineKeyboardButton('Back to the menu',callback_data=f'start.{message.chat.id}'),
            types.InlineKeyboardButton('Send',callback_data=f'send.{message.chat.id}'),)
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.id,text=f"{x}",reply_markup=mrk)


def calc(message,text):
    numlist = ['0','1','2','3','4','5','6','7','8','9','0']
    letlist = ['/','-','+','=','*','^']
    mrk = types.InlineKeyboardMarkup(row_width=1)
    mrk.row(types.InlineKeyboardButton('1',callback_data=f'1.{message.chat.id}'),
            types.InlineKeyboardButton('2',callback_data=f'2.{message.chat.id}'),
            types.InlineKeyboardButton('3',callback_data=f'3.{message.chat.id}'),
            types.InlineKeyboardButton('+',callback_data=f'+.{message.chat.id}'),
            types.InlineKeyboardButton("-",callback_data=f'-.{message.chat.id}'))
    mrk.row(types.InlineKeyboardButton('4',callback_data=f'4.{message.chat.id}'),
            types.InlineKeyboardButton('5',callback_data=f'5.{message.chat.id}'),
            types.InlineKeyboardButton('6',callback_data=f'6.{message.chat.id}'),
            types.InlineKeyboardButton('*',callback_data=f'*.{message.chat.id}'),
            types.InlineKeyboardButton("/",callback_data=f'/.{message.chat.id}'))
    mrk.row(types.InlineKeyboardButton('7',callback_data=f'7.{message.chat.id}'),
            types.InlineKeyboardButton('8',callback_data=f'8.{message.chat.id}'),
            types.InlineKeyboardButton('9',callback_data=f'9.{message.chat.id}'),
            types.InlineKeyboardButton('0',callback_data=f'0.{message.chat.id}'),
            types.InlineKeyboardButton('^',callback_data=f'^.{message.chat.id}'))
    mrk.row( types.InlineKeyboardButton('=',callback_data=f'=.{message.chat.id}'),
            types.InlineKeyboardButton('CE',callback_data=f'CE.{message.chat.id}'),
             types.InlineKeyboardButton('menu',callback_data=f'start.{message.chat.id}'))

    if text == 'calc':
        text = 'Evaluator 3.0'
        var.b[message.chat.id]=bot.edit_message_text(chat_id=message.chat.id,
                                                     message_id=message.id,
                                                     text=text,
                                                     reply_markup=mrk)
    elif message.text == 'Evaluator 3.0' and text!='CE' \
            or '\n' in message.text and text!='CE' \
            or message.text == '0' and text!='CE' :
        var.b[message.chat.id]=bot.edit_message_text(chat_id=message.chat.id,
                                                     message_id=message.id,
                                                     text=text,
                                                     reply_markup=mrk)
    elif text == 'CE':
        var.b[message.chat.id]=bot.edit_message_text(chat_id=message.chat.id,
                                                     message_id=message.id,
                                                     text='0',
                                                     reply_markup=mrk)

    elif text == '=':
        eva = message.text
        eva = eva.replace('^','**')

        var.b[message.chat.id]=bot.edit_message_text(chat_id=message.chat.id,
                                                     message_id=message.id,
                                                     text=f'{message.text}\n{eval(eva)}',
                                                     reply_markup=mrk)
    else:
        if message.text[-1] in letlist and text in letlist:
            var.b[message.chat.id]=bot.edit_message_text(chat_id=message.chat.id,
                                                         message_id=message.id,
                                                         text=message.text[:-1]+text,
                                                         reply_markup=mrk)
        else:
            var.b[message.chat.id]=bot.edit_message_text(chat_id=message.chat.id,
                                                         message_id=message.id,
                                                         text=message.text+text,
                                                         reply_markup=mrk)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # print(call.data)
    # print(call.data[call.data.index('.')+1:])
    # print(call.data[:call.data.index('.')])
    bot.answer_callback_query(call.id)

    if call.data[:call.data.index('.')] == 'start':
        menu(var.b[int(call.data[call.data.index('.')+1:])])
    elif call.data[:call.data.index('.')] == 'help':
        hell(var.b[int(call.data[call.data.index('.')+1:])])
    elif call.data[:call.data.index('.')] == 'info':
        info(var.b[int(call.data[call.data.index('.')+1:])])
    elif call.data[:call.data.index('.')] == 'users':
        users(var.b[int(call.data[call.data.index('.')+1:])])
    elif call.data[:call.data.index('.')] == 'send':
        send(var.b[int(call.data[call.data.index('.')+1:])])
    else:
        calc(var.b[int(call.data[call.data.index('.')+1:])],call.data[:call.data.index('.')])


bot.infinity_polling()