from sqlalchemy.orm import Session

from src.domain.model import UserEntity
from src.infra.db import SqlAlchemyBaseRepository


class UserRepository(SqlAlchemyBaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, UserEntity)
