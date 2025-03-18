import asyncio
import uvicorn
from my_fast_api import f_api
from bot_instance import bot, dp, bot_storage_key
from command_handlers import ch_router
from postgress_table import init_models
from start_menu import set_main_menu


async def run_fastapi():
    """Запуск FastAPI в асинхронном режиме (в одном event loop с ботом)"""
    config = uvicorn.Config(f_api, host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await init_models()
    dp.startup.register(set_main_menu)

    await dp.storage.set_data(key=bot_storage_key, data={})

    dp.include_router(ch_router)

    # Запускаем FastAPI в фоновом режиме
    asyncio.create_task(run_fastapi())

    # Запускаем бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())  # Здесь и бот, и FastAPI работают в одном event loop

