from aiogram.filters import Command
from aiogram import Router,types,F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from additions.db import *
from additions.keyboards import *
from .states import *
from .callback_datas import q1,q2,q3

user_register_router=Router()
user_data={}

@user_register_router.message(Command("start"))
async def register_user1(msg:types.Message,state: FSMContext):
    wwww=get_the_user_info(msg.from_user.id)
    user_data[msg.from_user.id]={}
    user_data[msg.from_user.id]["username"]=msg.from_user.username

    if wwww==None:
        await state.set_state(RegisterForm.name)
        await msg.reply("Hi, enter your name...",reply_markup=ReplyKeyboardRemove())
    elif wwww[0]==2:
        user_data[msg.from_user.id]=get_the_user_info(msg.from_user.id)[1]
        await msg.answer("You can search for services by tapping on /see and update your profile using /update_profile tags ",
                                      reply_markup=ReplyKeyboardRemove())
    elif wwww[0]==1:
        user_data[msg.from_user.id]=get_the_user_info(msg.from_user.id)[1]
        await msg.answer("You can update your profile using /update_profile tag ",
                                      reply_markup=ReplyKeyboardRemove())
    elif wwww[0]==0:
        await msg.answer("""As an admin you can add region using /add_region or district using /add_district or skill using /add_skill""",
                                      reply_markup=ReplyKeyboardRemove())


@user_register_router.message(Command("update_profile"))
async def register_user1(msg:types.Message,state: FSMContext):
    user_data[msg.from_user.id]=get_the_user_info(msg.from_user.id)[1]
    user_data[msg.from_user.id]["username"]=msg.from_user.username
    await state.set_state(RegisterForm.name)
    await msg.reply("Enter your name...",reply_markup=ReplyKeyboardRemove())

@user_register_router.message(RegisterForm.name)
async def register_user2(msg:types.Message,state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(RegisterForm.contact_info)
    await msg.answer("Click the button to share your contact info",
                     reply_markup=share_contact_button())
    
@user_register_router.message(RegisterForm.contact_info)
async def register_user3(msg:types.Message,state: FSMContext):
    await state.update_data(contact_info=list(msg.contact))
    await state.set_state(RegisterForm.user_type)
    await msg.answer("Choose one to countinue: ", reply_markup=get_the_user_type())


@user_register_router.callback_query(F.data.startswith("user_type_is__"))
async def register_user4(callback:types.callback_query,state: FSMContext):
    _,user_type=callback.data.split("__")
    if user_type=="service":
        regions=get_all_regions()
        skills=get_all_skills()
        if regions and skills:
            data1,data2=paginate_data(regions,12)
            text=generate_text1(data1)

            user_data[callback.from_user.id]["rpn"]=12
            await update_message(callback.message,f"Choose one region to countinue:\n{text}",data1,q1,data2)
            await state.update_data(user_type=user_type)
            await state.set_state(RegisterForm.region)
        else:
            await update_message1(callback.message,f"Registraion cannot be completed due to lack of information which should be provided by admin!")

    else:
        data=await state.get_data()
        create_customer_object(telegram_id=callback.from_user.id,
                               name=data["name"],
                               phone_number=data["contact_info"][0][1],
                               telegram_username=callback.from_user.username)

        delete_user(telegram_id=callback.from_user.id,
                    phone_number=data["contact_info"][0][1],
                    data='service'
                    )
        await state.clear()
        await update_message1(callback.message,"Registration is complete!")
        await callback.message.answer("You can search for services by tapping on /services or update your profile using /update_profile tag ",
                                      reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@user_register_router.callback_query(F.data.startswith("s_regions_page__"))
async def register_user4(callback:types.callback_query,state: FSMContext):
    _,page=callback.data.split("__")
    user_data[callback.from_user.id]["rpn"]+=12 if page=="next" else -12
    regions=get_all_regions()
    data1,data2=paginate_data(regions,user_data[callback.from_user.id]["rpn"])
    text=generate_text1(data1)
    await update_message(callback.message,f"Choose one region to countinue:\n{text}",data1,q1,data2)
    await state.set_state(RegisterForm.districts)

    await callback.answer()



@user_register_router.callback_query(F.data.startswith("s_region_num_"))
async def register_user5(callback:types.callback_query,state: FSMContext):
    _,region_id=callback.data.split("__")
    region=get_the_region(region_id)
    user_data[callback.from_user.id]["rin"]=region_id
    user_data[callback.from_user.id]["dpn"]=12
    districts,data2=paginate_data(get_all_districts(region_id),12)
    if len(districts)>0:
        text=generate_text1(districts)
        user_data[callback.from_user.id]["districts"]=[]
        await update_message(callback.message,f"Choose districts you can serve(you can choose more than one...):\n{text}",districts,q2[:-1],data2)
    else:
        await update_message1(callback.message,"No districts found...(Only admin can register districts)")
   
    await state.update_data(region=region)
    await state.set_state(RegisterForm.districts)
    await callback.answer()




@user_register_router.callback_query(F.data.startswith("s_districts_page__"))
async def register_user6(callback:types.callback_query,state: FSMContext):
    region_id=user_data[callback.from_user.id]["rin"]
    region=get_the_region(region_id)
    user_data[callback.from_user.id]["dpn"]+=12 if callback.data.split("__")[1]=="next" else -12
    districts,data2=paginate_data(get_all_districts(region_id),user_data[callback.from_user.id]["dpn"])
    q=None
    q=q2[:-1] if len(user_data[callback.from_user.id]["districts"])<1 else q2
        
    text=f"""Choose districts you can serve(you can choose more than one):
Choosen ones:({generate_text1(user_data[callback.from_user.id]["districts"])})\n
{generate_text1(districts)}"""
    await update_message(callback.message,text,districts,q,data2)
    
    await state.update_data(region=region)
    await state.set_state(RegisterForm.districts)
    await callback.answer()



@user_register_router.callback_query(F.data.startswith("s_district_num_"))
async def register_user7(callback:types.callback_query,state: FSMContext):
    region_id=user_data[callback.from_user.id]["rin"]
    _,district_id=callback.data.split("__")
    district=get_the_district(district_id)

    if district not in user_data[callback.from_user.id]["districts"] and len(user_data[callback.from_user.id]["districts"])<6:
        user_data[callback.from_user.id]["districts"].append(district)
    else:
        user_data[callback.from_user.id]["districts"].remove(district)

    districts,data2=paginate_data(get_all_districts(region_id),user_data[callback.from_user.id]["dpn"])
    text=f"""Choose districts you can serve(you can choose more than one):
Choosen ones:({generate_text1(user_data[callback.from_user.id]["districts"])})\n
{generate_text1(districts)}"""
    q=None
    q=q2[:-1] if len(user_data[callback.from_user.id]["districts"])<1 else q2
        
    await update_message(callback.message,text,districts,q,data2)
    
    await state.update_data(districts=user_data[callback.from_user.id]["districts"])
    await state.set_state(RegisterForm.skills)
    await callback.answer()


@user_register_router.callback_query(F.data.startswith("districts_has_been_chosen"))
async def register_user8(callback:types.callback_query,state: FSMContext):
    user_data[callback.from_user.id]["skills"]=[]
    user_data[callback.from_user.id]["spn"]=12
    skills,data2=paginate_data(get_all_skills(),12)
    if len(skills)>0:
        text=generate_text1(skills)
        await update_message(callback.message,f"Choose skills you can perform(you can choose more than one...):\n{text}",skills,q3[:-1],data2)
    else:
        await update_message1(callback.message,"No skills found...(Only admin can regitser skills!)")
    await state.update_data(districts=user_data[callback.from_user.id]["districts"])
    await state.set_state(RegisterForm.skills)
    await callback.answer()
    

@user_register_router.callback_query(F.data.startswith("s_skills_page__"))
async def register_user9(callback:types.callback_query,state: FSMContext):
    user_data[callback.from_user.id]["spn"]+=12 if callback.data.split("__")[1]=="next" else -12
    skills,data2=paginate_data(get_all_skills(),user_data[callback.from_user.id]["spn"])

    text=f"""Choose skills you can perform(you can choose more than one):
Choosen ones:({generate_text1(user_data[callback.from_user.id]["skills"])})\n
{generate_text1(skills)}"""
    q=None
    q=q3[:-1] if len(user_data[callback.from_user.id]["skills"])<1 else q3
    await update_message(callback.message,text,skills,q,data2)
    
    await state.update_data(districts=user_data[callback.from_user.id]["districts"])
    await state.set_state(RegisterForm.skills)
    await callback.answer()



@user_register_router.callback_query(F.data.startswith("s_skills_num_"))
async def register_user10(callback:types.callback_query,state: FSMContext):
    _,skill_id=callback.data.split("__")
    skill=get_the_skill(skill_id)

    if skill not in user_data[callback.from_user.id]["skills"] and len(user_data[callback.from_user.id]["skills"])<6 :
        user_data[callback.from_user.id]["skills"].append(skill)
    else:
        user_data[callback.from_user.id]["skills"].remove(skill)

    skills,data2=paginate_data(get_all_skills(),user_data[callback.from_user.id]["spn"])
    text=f"""Choose skills you can perform(you can choose more than one, less than 7):
Choosen ones:({generate_text1(user_data[callback.from_user.id]["skills"])})\n
{generate_text1(skills)}"""
    q=None
    q=q3[:-1] if len(user_data[callback.from_user.id]["skills"])<1 else q3
    await update_message(callback.message,text,skills,q,data2)
    await state.update_data(districts=user_data[callback.from_user.id]["districts"])
    await state.set_state(RegisterForm.skills)
    await callback.answer()


@user_register_router.callback_query(F.data.startswith("skills_has_been_chosen"))
async def register_user11(callback:types.callback_query,state: FSMContext):   
    await update_message1(callback.message,"Now enter description abour you(only 300 characters allowed):")
    await state.update_data(skills=user_data[callback.from_user.id]["skills"])
    await state.set_state(RegisterForm.description)
    await callback.answer()


@user_register_router.message(RegisterForm.description)
async def register_user12(msg: types.Message, state: FSMContext):
    data= await state.get_data()
    message=format_the_message(data,user_data[msg.from_user.id]["username"],msg.text[:300])

    if create_service_object(telegram_id= msg.from_user.id,
                             name=data["name"],
                             phone_number=data["contact_info"][0][1],
                             telegram_username=msg.from_user.username,
                             description=msg.text,
                             districts_ids=make_it_list(data["districts"]),
                             skills_ids=make_it_list(data["skills"])):
        delete_user(telegram_id=msg.from_user.id,
            phone_number=data["contact_info"][0][1],
            data='customer'
            )
        
        await msg.answer(f"Your info:\n{message}",reply_markup=ReplyKeyboardRemove())
        await msg.answer("Registration is complete!\nYou can update your profile using /update_profile tag ",reply_markup=ReplyKeyboardRemove())
        await state.clear()
