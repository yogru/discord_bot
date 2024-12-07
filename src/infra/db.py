from __future__ import annotations

import abc
import logging
import uuid
from typing import List
from sqlalchemy.orm import declarative_base, Session, sessionmaker
from sqlalchemy import Column, DateTime, func, Boolean, Engine, create_engine, MetaData, text, TypeDecorator, String
from sqlalchemy.dialects.postgresql import UUID

from src.infra.env import EnvSettings


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def flush(self):
        raise NotImplementedError


BaseTable = declarative_base()


class BaseEntity(BaseTable):
    __abstract__ = True  # 이 클래스는 테이블이 생성되지 않도록 설정 (추상 클래스)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def setup_delete(self, to_delete: bool = True):
        self.deleted = to_delete


class SqlAlchemyBaseRepository:
    def __init__(self, session: Session, model: BaseEntity):
        self.session = session
        self.model = model

    def add(self, model: BaseEntity):
        self.session.add(model)
        return model

    def add_all(self, models: List[BaseEntity]):
        self.session.add_all(models)

    def delete(self, model: BaseEntity):
        self.session.delete(model)

    def get(self, pk: UUID) -> BaseEntity:
        return (
            self.session
            .query(self.model)
            .filter_by(id=pk)
            .first()
        )


class StringifiedEnum(TypeDecorator):
    impl = String
    cache_ok = True

    def __init__(self, enumclass, *args, **kwargs):
        self._enumclass = enumclass
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if isinstance(value, self._enumclass):
            return value.value  # Enum을 문자열로 변환
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self._enumclass(value)  # 문자열을 Enum으로 변환
        return value


########################################################################################################################
logging.basicConfig()
logger = logging.getLogger(__name__)


def get_pg_db_url(env: EnvSettings):
    return f"postgresql+psycopg2://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@" \
           f"{env.DATABASE_ADDRESS}/{env.DATABASE_NAME}"


def create_engine_by_env(env: EnvSettings) -> Engine:
    echo = False
    if env.APP_MODE == 'prod':
        echo = False

    return create_engine(
        get_pg_db_url(env),
        echo=echo
    )


def create_session_maker(engine_: Engine, env: EnvSettings):
    return sessionmaker(autocommit=env.DATABASE_AUTO_COMMIT,
                        autoflush=env.DATABASE_AUTO_FLUSH,
                        bind=engine_
                        )


def create_persistence_by_env(env: EnvSettings = EnvSettings.load_env(app_mode='local')):
    engine = create_engine_by_env(env)
    session_maker = create_session_maker(engine, env)
    return engine, session_maker


def create_tables(env: EnvSettings):
    # 사고 방지..
    # if env.APP_MODE == "prod":
    #     logger.info("Production mode - Create Tables aborted!")
    #     return
    engine = create_engine_by_env(env)
    BaseTable.metadata.create_all(engine)


def drop_tables(env: EnvSettings):
    drop_truncate_tables(env=env)


def truncate_tables(env: EnvSettings):
    drop_truncate_tables(env=env, only_truncate=True)


def drop_truncate_tables(env: EnvSettings, only_truncate: bool = False):
    # if env.APP_MODE == "prod":
    #     logger.info("Production mode - Truncate and Drop aborted!")
    #     return
    engine = create_engine_by_env(env)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    sm = sessionmaker(bind=engine)
    session = sm()
    # 모든 테이블 순서대로 튜런케이트 후 드롭
    with engine.connect() as conn:
        trans = conn.begin()  # 트랜잭션 시작
        try:
            # 외래 키 무시 (필요한 경우)
            conn.execute(text('SET session_replication_role = replica;'))
            for table in reversed(metadata.sorted_tables):
                conn.execute(text(f"TRUNCATE TABLE {table.name} CASCADE;"))
                if only_truncate:
                    continue
                conn.execute(text(f"DROP TABLE {table.name} CASCADE;"))
            conn.execute(text('SET session_replication_role = DEFAULT;'))  # 외래 키 검사를 다시 활성화
            trans.commit()
        except Exception as e:
            trans.rollback()
            logger.info(f"Error occurred: {e}")
            raise
        finally:
            session.close()
