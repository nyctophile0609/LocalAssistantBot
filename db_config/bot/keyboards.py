import logging
import asyncio
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


from aconfigreader import config
import sqlite3
from datetime import datetime
from aconfigreader import config
from db import *

def number_board(num:int,data_callback:list,checks_it:list,call_string:str):
    builder=InlineKeyboardBuilder()
    for i in range (num):
        if i%2<1:
            builder.row(types.InlineKeyboardButton(text=f'{i+1}',callback_data=f'{call_string}_{i}'))
        
        elif i%2:
            builder.add(types.InlineKeyboardButton(text=f'{i+1}',callback_data=f'{call_string}_{i}'))
   
   
    if checks_it==[1,0]:
        builder.row(types.InlineKeyboardButton(text=f'Back',callback_data=data_callback[0]))
    elif checks_it==[0,1]:
        builder.row(types.InlineKeyboardButton(text=f'Next',callback_data=data_callback[1]))
    elif checks_it==[1,1]:
        builder.row(types.InlineKeyboardButton(text=f'Back',callback_data=data_callback[0]),
        types.InlineKeyboardButton(text='Next',callback_data=data_callback[1]))

    return builder.as_markup()







def cr_inline_keyboard(data:list,call_data:list,checks_it:list):
    builder=InlineKeyboardBuilder()
    x=len(data)
    for i in range (x):
        if i%4<1:
            builder.row(types.InlineKeyboardButton(text=f'{i+1}',callback_data=f'{call_data[2]}_{data[i][0]}'))
        elif i%4<2:
            builder.add(types.InlineKeyboardButton(text=f'{i+1}',callback_data=f'{call_data[2]}_{data[i][0]}'))
        elif i%4<3:
            builder.add(types.InlineKeyboardButton(text=f'{i+1}',callback_data=f'{call_data[2]}_{data[i][0]}'))
        elif i%4:
            builder.add(types.InlineKeyboardButton(text=f'{i+1}',callback_data=f'{call_data[2]}_{data[i][0]}'))
        
    if checks_it==[1,0]:
        builder.row(types.InlineKeyboardButton(text=f'Back',callback_data=call_data[0]))
    elif checks_it==[0,1]:
        builder.row(types.InlineKeyboardButton(text=f'Next',callback_data=call_data[1]))
    elif checks_it==[1,1]:
        builder.row(types.InlineKeyboardButton(text=f'Back',callback_data=call_data[0]),
        types.InlineKeyboardButton(text='Next',callback_data=call_data[1]))
    if len(call_data)==4:
        builder.row(types.InlineKeyboardButton(text=f'Done',callback_data=call_data[3]))


    return builder.as_markup()





def generate_text1(data:list,):
    message=""
    for j,i in enumerate(data):
        message+=f"{j+1}. {i[1]}\n"
    return message


    pass
def paginate_data(data:list,pn:int):
    qw=value=None
    if len(data[pn-12:])>=12:
        qw=data[pn-12:12]
    else:
        qw=data[pn-12:]
    
    if pn==12 and len(data)>12:
        value=[0,1]
    elif 12<len(data)<=pn:
        value=[1,0]
    elif len(data)<12:
        value=[0,0]
    else:
        value=[1,1]
    return [qw,value]
    



async def update_questions1(message:types.Message,data:list,text:str,call_data:list,checks_it:list):
    with suppress(TelegramBadRequest):
        await message.edit_text(text,reply_markup=cr_inline_keyboard(data,call_data,checks_it))
