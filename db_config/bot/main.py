import logging
import asyncio
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import exceptions
from keyboards import *
import sqlite3
from datetime import datetime
from aconfigreader import config
from db import *



logging.basicConfig(level=logging.INFO)
bot=Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
dp=Dispatcher()
user_data={}
l1=["regionpage_back","regiopage_next","regions"]
l2=["districtpage_back","districtpage_next","districts"]
l30=["skillpage_back","skillpage_next","skills"]
l31=["skillpage_back","skillpage_next","skills","choosing_skill_finished"]
l4=["masterpage_back","masterpage_next","masters"]



@dp.message(Command('start'))
async def cmd_start(message:types.Message):
    if get_the_user_info(message.from_user.id)==None:
        
        #registration
        pass
    else:





        data=get_the_user_info(message.from_user.id)

        status,user_data[message.from_user.id]=data
        user_data[message.from_user.id]["chosen_skills"]=list()
        if status==0:
            pass
        if status==1:
            pass
        if status==2:
            data1,data2=paginate_data(get_all_regions(),12)
            text=generate_text1(data1)
            data1=get_all_regions()
            await message.reply(f'Hi, {user_data[message.from_user.id]["name"]}\nChoose on region to continue:\n{text}',
                                reply_markup=cr_inline_keyboard(data1,l1,[0,0]))
            




@dp.callback_query(F.data.startswith("regions_"))
async def cs_district1(callback:types.callback_query):
    _,region_num=callback.data.split("_")
    pn=user_data[callback.from_user.id]["dpn"]=12
    user_data[callback.from_user.id]["rin"]=region_num
    data1,data2=paginate_data(get_all_districts(region_num),pn=12)
    text=f"Choose your district to countinue:\n{generate_text1(data1)}"
    await update_questions1(callback.message,data1,text,l2,data2)
    await callback.answer()

@dp.callback_query(F.data.startswith("districtpage_"))
async def cs_districts2(callback:types.callback_query):
    _,x=callback.data.split("_")
    user_data[callback.from_user.id]["dpn"]+=12 if x=="next" else -12
    pn,rin=user_data[callback.from_user.id]["dpn"],user_data[callback.from_user.id]["rin"]    
    data1,data2=paginate_data(get_all_districts(rin),pn=pn)
    text=f"Choose your district to countinue:\n{generate_text1(data1)}"
    await update_questions1(callback.message,data1,text,l2,data2)
    await callback.answer()


@dp.callback_query(F.data.startswith("districts_"))
async def cs_skills1(callback:types.callback_query):
    _,x=callback.data.split("_")
    pn=user_data[callback.from_user.id]["spn"]=12 
    user_data[callback.from_user.id]["din"]=x
    data1,data2=paginate_data(get_all_skills(),pn)
    text=generate_text1(data1)
    text=f"Choose the skills (you can choose more than one...)\n{text}"
    await update_questions1(callback.message,data1,text,l30,data2)
    await callback.answer()

@dp.callback_query(F.data.startswith("skillpage_"))
async def cs_skills2(callback:types.callback_query):
    _,x=callback.data.split("_")
    user_data[callback.from_user.id]["spn"]+=12 if x=="next" else -12
    pn=user_data[callback.from_user.id]["spn"]
    data1,data2=paginate_data(get_all_skills(),pn)
    text10=generate_text1(user_data[callback.from_user.id]["chosen_skills"])
    text11 =f"\nChosen skills: {text10}\n" if text10 !="" else None
    l3=l31 if len(user_data[callback.from_user.id]["chosen_skills"])>0 else l30
    text = f"""Choose the skills to continue:
    {text11 if text11!=None else ""}
    {generate_text1(data1)}"""
    await update_questions1(callback.message,data1,text,l3,data2)
    await callback.answer()


@dp.callback_query(F.data.startswith("skills"))
async def cs_skill3(callback: types.callback_query):
    _, sin = callback.data.split("_")
    pn = user_data[callback.from_user.id]["spn"]
    data1, data2 = paginate_data(get_all_skills(), pn)
    skill = get_the_skill(sin)
    # print(user_data[callback.from_user.id])
    if skill in user_data[callback.from_user.id]["chosen_skills"]:
        user_data[callback.from_user.id]["chosen_skills"].remove(skill)  
    elif len(user_data[callback.from_user.id]["chosen_skills"])<6:
        user_data[callback.from_user.id]["chosen_skills"].append(skill)  
    # print(user_data[callback.from_user.id])  
    text10=generate_text1(user_data[callback.from_user.id]["chosen_skills"])
    text11 =f"\nChosen skills: {text10}\n" if text10 !="" else None
    l3=l31 if len(user_data[callback.from_user.id]["chosen_skills"])>0 else l30
    text = f"""Choose the skills to continue:
    {text11 if text11!=None else ""}
    {generate_text1(data1)}"""
    await update_questions1(callback.message, data1, text, l3, data2)
    await callback.answer()


@dp.callback_query(F.data=="choosing_skill_finished")
async def cs_masters1(callback: types.callback_query):
    skills=user_data[callback.from_user.id]["chosen_skills"]
    rin=user_data[callback.from_user.id]["rin"]
    din=user_data[callback.from_user.id]["din"]
    masters=get_the_masters(rin,din,skills)
    pn=user_data[callback.from_user.id]["mpn"]=12
    data1,data2=paginate_data(masters,pn)
    text1=generate_text1(data1)
    text=f"Choose the master to get their contact info:\n{text1}"
    await update_questions1(callback.message,data1,text,l4,data2)
    await callback.answer()


@dp.callback_query(F.data.startswith("masterpage_"))
async def cs_master2(callback: types.callback_query):
    _,x=callback.data.split("_")
    user_data[callback.from_user.id]["mpn"]+=12 if x=="next" else -12
    skills=user_data[callback.from_user.id]["chosen_skills"]
    rin=user_data[callback.from_user.id]["rin"]
    din=user_data[callback.from_user.id]["din"]
    masters=get_the_masters(rin,din,skills)
    data1,data2=paginate_data(masters,user_data[callback.from_user.id]["mpn"])
    text1=generate_text1(data1)
    text=f"Choose the master to get their contact info:\n{text1}"
    await update_questions1(callback.message,data1,text,l4,data2)
    await callback.answer()

@dp.callback_query(F.data.startswith("masters_"))
async def cs_master3(callback: types.callback_query):
    _,w=callback.data.split("_")
    sc=get_the_service(w)
    await callback.message.answer(f"""
Name: {sc[0][1]}
Number: {sc[0][3]}
Username: {sc[0][4]}
Serving since: {sc[0][6]}
Description: {sc[0][5]}

Skills: {sc[3]}

Available in {sc[2]}

of {sc[1][1]} region

""")

    await callback.answer()














    


async def main():
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(main())