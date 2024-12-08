from sqlalchemy.orm import Session

from src.domain.repository import UserRepository, FileRepository, LLMRepository
from src.infra.db import AbstractUnitOfWork


class SqlAlchemyUow(AbstractUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.users = UserRepository(self.session)
        self.files = FileRepository(self.session)
        self.llm_repo = LLMRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def detach_from_persistence(self):
        self.session.expunge_all()

    def rollback(self):
        self.session.rollback()

    def flush(self):
        self.session.flush()
