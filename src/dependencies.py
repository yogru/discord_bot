from src.app.usecase.user_usecase import UserUseCase
from src.infra.db import create_persistence_by_env
from src.infra.env import EnvSettings
from src.infra.gpt import GPT
from src.uow import SqlAlchemyUow

env = EnvSettings()
gpt = GPT(env=env)

# db
engine, session_maker = create_persistence_by_env(env)
uow = SqlAlchemyUow(session_maker)

user_use_case = UserUseCase(
    uow=uow
)
