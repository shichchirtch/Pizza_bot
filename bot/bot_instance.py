from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis, StorageKey
from aiogram.fsm.storage.base import DefaultKeyBuilder
from config import settings

key_builder = DefaultKeyBuilder(with_destiny=True)

using_redis = Redis(host=settings.REDIS_HOST)

redis_storage = RedisStorage(redis=using_redis, key_builder=key_builder)


class FSM_ST(StatesGroup):
    after_start = State()
    admin = State()


bot_tocken = settings.BOT_TOKEN

bot = Bot(token=bot_tocken,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

bot_storage_key = StorageKey(bot_id=bot.id, user_id=bot.id, chat_id=bot.id)

dp = Dispatcher(storage=redis_storage)

server_cart = {}

