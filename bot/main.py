import asyncio
from aiogram import Bot,Dispatcher
from bot_instance import bot
from handlers.user_register import user_register_router
from handlers.customer_side import customer_side_router
from handlers.admin_side import admin_side_router
def register_routers(dp:Dispatcher):
    dp.include_router(user_register_router)
    dp.include_router(customer_side_router)
    dp.include_router(admin_side_router)
async def main():
    dp=Dispatcher()
    register_routers(dp)

    await dp.start_polling(bot,skip_updates=False)



if __name__=="__main__":
    asyncio.run(main())

    