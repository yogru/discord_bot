from src.app.usecase.auth_usecase import AuthUseCase
from src.app.usecase.chat_usecase import ChatUseCase
from src.app.usecase.file_usecase import FileUseCase
from src.app.usecase.user_usecase import UserUseCase
from src.infra.db import create_persistence_by_env
from src.infra.env import EnvSettings
from src.infra.gpt import GPT
from src.infra.object_storage import MinIoWrapper
from src.uow import SqlAlchemyUow

env = EnvSettings()
gpt = GPT(env=env)
min_io = MinIoWrapper(env=env)
min_io.init()

# db
engine, session_maker = create_persistence_by_env(env)
uow = SqlAlchemyUow(session_maker)

file_use_case = FileUseCase(
    uow=uow,
    min_io=min_io,
)
user_use_case = UserUseCase(
    uow=uow
)
auth_use_case = AuthUseCase(
    uow=uow,
)

chat_use_case = ChatUseCase(
    uow=uow,
    env=env
)
