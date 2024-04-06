from aiogram.filters import Command
from aiogram import Router,types,F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from additions.db import *
from additions.keyboards import *
from .states import *
from .callback_datas import *

admin_side_router=Router()
user_data={}


@admin_side_router.message(Command("add_region"))
async def admin_add_region1(msg:types.Message,state: FSMContext):
    wwww=get_the_user_info(msg.from_user.id)
    if wwww[0]==0:
        await state.set_state(AdminAddRegion.region)
        await msg.answer("Enter region name...(Only 40 characters allowed!)",reply_markup=ReplyKeyboardRemove())

@admin_side_router.message(AdminAddRegion.region)
async def admin_add_region2(msg:types.Message,state: FSMContext):
    if create_region_object(msg.text[:40]):
        await msg.answer("""Region added successefully!\nAs an admin you can add region using /add_region or district using /add_district or skill using /add_skill""")
        await state.clear()
    
@admin_side_router.message(Command("add_district"))
async def admin_add_district1(msg:types.Message,state: FSMContext):
    wwww=get_the_user_info(msg.from_user.id)
    if wwww[0]==0:
        regions=get_all_regions()
        text=generate_text1(regions)
        await msg.answer(f"Choose one region to countinue:\n{text}",reply_markup=cr_inline_keyboard(regions,a1,[0,0]))
        await state.set_state(AdminAddDistrict.region)


@admin_side_router.callback_query(F.data.startswith("a_region_num"))
async def admin_add_district2(callback:types.callback_query,state: FSMContext):
    _,region_id=callback.data.split("__")
    await update_message1(callback.message,"Enter the name of district...(Only 40 characters allowed!)")
    await state.update_data(region=region_id)
    await state.set_state(AdminAddDistrict.district)

@admin_side_router.message(AdminAddDistrict.district)
async def admin_add_district3(msg:types.Message,state: FSMContext):

    data=await state.get_data()
    if create_district_object(msg.text[:40],data["region"]):
        await msg.answer("""District added successefully!\nAs an admin you can add region using /add_region or district using /add_district or skill using /add_skill""")
        await state.clear()

@admin_side_router.message(Command("add_skill"))
async def admin_add_skill1(msg:types.Message,state: FSMContext):
    wwww=get_the_user_info(msg.from_user.id)
    if wwww[0]==0:
        await state.set_state(AdminAddSkill.skill)
        await msg.answer("Enter skill name...(Only 40 characters allowed!)")

@admin_side_router.message(AdminAddSkill.skill)
async def admin_add_skill2(msg:types.Message,state: FSMContext):
    if create_skill_object(msg.text[:40]):
        await msg.answer("""Skill added successefully!\nAs an admin you can add region using /add_region or district using /add_district or skill using /add_skill""")
        await state.clear()


