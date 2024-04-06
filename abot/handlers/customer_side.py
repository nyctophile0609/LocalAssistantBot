from aiogram.filters import Command
from aiogram import Router,types,F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from additions.db import *
from additions.keyboards import *
from .states import *
from .callback_datas import *

customer_side_router=Router()
cs_data={}

@customer_side_router.message(Command("services"))
async def cs_district1(msg:types.Message):
    if get_the_user_info(msg.from_user.id):
        cs_data[msg.from_user.id]=get_the_user_info(msg.from_user.id)[1]
        if get_the_user_info(msg.from_user.id)[0]==2:
            cs_data[msg.from_user.id]['rpn']=12
            data1,data2=paginate_data(get_all_regions(),12)
            if len(data1)>0:
                text=generate_text1(data1)
                await msg.reply(f'Choose on region to continue:\n{text}',
                                    reply_markup=cr_inline_keyboard(data1,cs1,data2))
            else:
                await msg.reply("Not regions found...(Only admin can register regions)",reply_markup=ReplyKeyboardRemove())
    else:
        await msg.reply('You have not registered yet.\nYou can register using /start command...')

@customer_side_router.callback_query(F.data.startswith("regionpage_"))
async def cs_districts3(callback:types.callback_query):
    _,x=callback.data.split("_")
    cs_data[callback.from_user.id]["rpn"]+=12 if x=="next" else -12
    pn=cs_data[callback.from_user.id]["rpn"]   
    data1,data2=paginate_data(get_all_regions(),pn)
    text=generate_text1(data1)
    await update_message(callback.message,f'Choose on region to continue:\n{text}',data1,cs1,data2)
    await callback.answer()



@customer_side_router.callback_query(F.data.startswith("regions_"))
async def cs_district2(callback:types.callback_query):
    _,region_num=callback.data.split("_")
    pn=cs_data[callback.from_user.id]["dpn"]=12
    cs_data[callback.from_user.id]["rin"]=region_num
    data1,data2=paginate_data(get_all_districts(region_num),pn=12)
    if len(data1)>0:
        text=f"Choose your district to countinue:\n{generate_text1(data1)}"
        await update_message(callback.message,text,data1,cs2,data2)
    else:
        await update_message1(callback.message,"Not districts found...(Only admin can register districts)")
    await callback.answer()

@customer_side_router.callback_query(F.data.startswith("districtpage_"))
async def cs_districts3(callback:types.callback_query):
    _,x=callback.data.split("_")
    cs_data[callback.from_user.id]["dpn"]+=12 if x=="next" else -12
    pn,rin=cs_data[callback.from_user.id]["dpn"],cs_data[callback.from_user.id]["rin"]    
    data1,data2=paginate_data(get_all_districts(rin),pn=pn)
    text=f"Choose your district to countinue:\n{generate_text1(data1)}"
    await update_message(callback.message,text,data1,cs2,data2)
    await callback.answer()


@customer_side_router.callback_query(F.data.startswith("districts_"))
async def cs_skills1(callback:types.callback_query):
    _,x=callback.data.split("_")
    pn=cs_data[callback.from_user.id]["spn"]=12 
    cs_data[callback.from_user.id]["din"]=x
    data1,data2=paginate_data(get_all_skills(),pn)
    text=generate_text1(data1)
    cs_data[callback.from_user.id]["chosen_skills"]=[]
    text=f"Choose the skills (you can choose between 1 and 6 skills...)\n{text}"
    await update_message(callback.message,text,data1,cs3,data2)
    await callback.answer()
 
@customer_side_router.callback_query(F.data.startswith("skillpage_"))
async def cs_skills2(callback:types.callback_query):
    _,x=callback.data.split("_")
    cs_data[callback.from_user.id]["spn"]+=12 if x=="next" else -12
    pn=cs_data[callback.from_user.id]["spn"]
    data1,data2=paginate_data(get_all_skills(),pn)
    text10=generate_text1(cs_data[callback.from_user.id]["chosen_skills"])
    text11 =f"\nChosen skills: {text10}\n" if text10 !="" else None
    l3=cs4 if len(cs_data[callback.from_user.id]["chosen_skills"])>0 else cs3
    if len(data1)>0:
        text = f"""Choose the skills to continue:
        {text11 if text11!=None else ""}
        {generate_text1(data1)}"""
        await update_message(callback.message,text,data1,l3,data2)
    else:
        await update_message1("Not skills found...(Only admin can register skills)")
    await callback.answer()


@customer_side_router.callback_query(F.data.startswith("skills"))
async def cs_skill3(callback: types.callback_query):
    _, sin = callback.data.split("_")
    pn = cs_data[callback.from_user.id]["spn"]
    data1, data2 = paginate_data(get_all_skills(), pn)
    skill = get_the_skill(sin)
    if skill in cs_data[callback.from_user.id]["chosen_skills"]:
        cs_data[callback.from_user.id]["chosen_skills"].remove(skill)  
    elif len(cs_data[callback.from_user.id]["chosen_skills"])<6:
        cs_data[callback.from_user.id]["chosen_skills"].append(skill)  
    text10=generate_text1(cs_data[callback.from_user.id]["chosen_skills"])
    text11 =f"\nChosen skills: {text10}\n" if text10 !="" else None
    l3=cs4 if len(cs_data[callback.from_user.id]["chosen_skills"])>0 else cs3
    text = f"""Choose the skills to continue:
    {text11 if text11!=None else ""}
    {generate_text1(data1)}"""
    await update_message(callback.message,text, data1, l3, data2)
    await callback.answer()


@customer_side_router.callback_query(F.data=="choosing_skill_finished")
async def cs_masters1(callback: types.callback_query):
    skills=cs_data[callback.from_user.id]["chosen_skills"]
    din=cs_data[callback.from_user.id]["din"]
    masters=get_all_services(din,skills)
    pn=cs_data[callback.from_user.id]["mpn"]=12
    if masters:
        data1,data2=paginate_data(masters,pn)
        text1=generate_text1(data1)
        text=f"Choose the master to get their contact info:\n{text1}"
        await update_message(callback.message,text,data1,cs5,data2)
    else:
        await update_message1(callback.message,("There are no services with the set of skills you have chose in that area!"))

    await callback.answer()


@customer_side_router.callback_query(F.data.startswith("masterpage_"))
async def cs_master2(callback: types.callback_query):
    _,x=callback.data.split("_")
    cs_data[callback.from_user.id]["mpn"]+=12 if x=="next" else -12
    skills=cs_data[callback.from_user.id]["chosen_skills"]
    rin=cs_data[callback.from_user.id]["rin"]
    din=cs_data[callback.from_user.id]["din"]
    masters=get_all_services(rin,din,skills)
    data1,data2=paginate_data(masters,cs_data[callback.from_user.id]["mpn"])
    if len(data1)>0:
        text1=generate_text1(data1)
        text=f"Choose the master to get their contact info:\n{text1}"
        await update_message(callback.message,text,data1,cs5,data2)
    else:
        await update_message1("No masters found...(Cause can be area or skills you chose or choosing too much skills!)")
    await callback.answer()

@customer_side_router.callback_query(F.data.startswith("masters_"))
async def cs_master3(callback: types.callback_query):
    _,w=callback.data.split("_")
    await callback.message.answer(format_the_message1(get_the_service(w)))

    await callback.answer()

