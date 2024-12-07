from typing import Optional

from sqlalchemy.orm import Session, joinedload

from src.domain.model import UserEntity, FileEntity
from src.infra.db import SqlAlchemyBaseRepository


class UserRepository(SqlAlchemyBaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, UserEntity)

    def find_by_id(self, user_id: str) -> Optional[UserEntity]:
        return (
            self.session.query(UserEntity)
            .filter(UserEntity.id == user_id)
            .options(joinedload(UserEntity.grants))
            .first()
        )


class FileRepository(SqlAlchemyBaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, FileEntity)