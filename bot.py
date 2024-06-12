import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.filters import IS_MEMBER, IS_ADMIN
from aiogram import types
from config import BOT_TOKEN, ADMINS
from sql_db import Database

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
db = Database()

async def main():
    db.create_table_users()
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.reply("Assalomu aleykum brat ishla yaxshimi !")

@dp.message(Command("getusers"))
async def get_top_users_command(message: types.Message):
    if message.from_user.id in ADMINS:
        users = db.get_top_member_added_users()
        print(25, users)
        message_text = f"Guruhga eng ko'p odam qo'shgan foydalanuvchilar:\n"
        for user in users:
            message_text += f"{user[1]}: {user[-1]}\n"
        await message.reply(message_text)
    else:
        await message.reply("Kechirasiz bu imkoniyat faqat guruh adminiga berilgan !")


@dp.message(F.new_chat_members)
async def new_member_message(message: types.Message):
    try:
        for member in message.new_chat_members:
            db.add_member_count(message.from_user.id)
        await message.delete()
    except Exception as ex:
        print(111, ex.args)

@dp.message(F.left_chat_member)
async def left_member_message(message: types.Message):
    try:
        await message.delete()
    except Exception as ex:
        print(111, ex.args)


@dp.message(F.text)
async def echo_message(message: types.Message):
    user_details = {
        "id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "username": message.from_user.username
    }
    db.get_or_create(user_details)

if __name__ == "__main__":
    asyncio.run(main())