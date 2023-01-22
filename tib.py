from aiogram.utils import executor
import logging
from config import dp, bot, ADMINS
from handlers import clients, callback, extra, admin, fsm_anketa
from database.bot_db import sql_create


async def on_sturtup(_):
    sql_create()
    await bot.send_message(chat_id=ADMINS[0],
                           text="Bot started!")


clients.register_handlers_client(dp)
callback.register_handlers_callback(dp)
admin.register_handlers_admin(dp)
fsm_anketa.register_handlers_anket(dp)

extra.register_message_handler(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_sturtup)
