from aiogram.fsm.state import State, StatesGroup

class RegisterForm(StatesGroup):
    name=State()
    contact_info=State()
    user_type=State()
    region=State()
    districts=State()
    skills=State()
    description=State()

class AdminAddRegion(StatesGroup):
    region=State()

class AdminAddDistrict(StatesGroup):
    region=State()
    district=State()

class AdminAddSkill(StatesGroup):
    skill=State()