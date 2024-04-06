from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from .db import *
from aiogram.types import ReplyKeyboardRemove

async def update_message(message:types.Message,text:str,data:list,call_data:list,checks_it:list):
    with suppress(TelegramBadRequest):
        await message.edit_text(text,reply_markup=cr_inline_keyboard(data,call_data,checks_it))

async def update_message1(message:types.Message,text:str,):
    with suppress(TelegramBadRequest):
        await message.edit_text(text)

async def delete_message1(message:types.Message,):
    with suppress(TelegramBadRequest):
        await message.delete()

def share_contact_button():
    builder=ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Share contact", request_contact=True))
    return builder.as_markup(resize_keyboard=True)

def get_the_user_type():
    builder=InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Service",callback_data="user_type_is__service"))
    builder.add(types.InlineKeyboardButton(text="Customer",callback_data="user_type_is__customer"))    
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


