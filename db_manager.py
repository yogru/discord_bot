from src.domain.model import *
from src.infra.db import create_persistence_by_env, drop_tables, create_tables, truncate_tables
from src.infra.env import EnvSettings, EnvironmentType
from src.uow import SqlAlchemyUow


def select_app_mode() -> EnvironmentType:
    app_mode_ = input('환경 선택 해주세요.(default == local) => [test, local, prod]: ')
    if app_mode_ in ["test", "local", "prod"]:
        return app_mode_
    return 'local'


def select_db_mode() -> str:
    print("cr:create, dr:drop, tr:truncate, init:데이터 삽입")
    db_mode_ = input('디비 모드.(default == tr) [tr, dr, cr, init]: ')
    if db_mode_ in ["tr", "dr", "cr", "init"]:
        return db_mode_
    return 'cr'


def init_data(env: EnvSettings):
    engine, session_maker = create_persistence_by_env(env=env)
    uow = SqlAlchemyUow(session_maker)


if __name__ == "__main__":
    """
     이 파일을 메인으로 실행 시키면 자유롭게 마이그레이션 가능하도록
    """
    app_mode = select_app_mode()
    db_mode = select_db_mode()
    env = EnvSettings.load_env(app_mode=app_mode)
    if db_mode == 'cr':
        drop_tables(env=env)
        create_tables(env=env)
    if db_mode == 'init':
        init_data(env=env)
    if db_mode == 'dr':
        drop_tables(env=env)
    if db_mode == 'tr':
        truncate_tables(env=env)
