from typing import Optional, List, Type

from sqlalchemy import func, and_
from sqlalchemy.orm import Session, joinedload

from src.domain.model import UserEntity, FileEntity, FileTagEntity, LLMQAEntity, LLMPromptEntity
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

    def find_by_tags(self, tags: List[str]) -> list[Type[FileEntity]]:
        return (
            self.session.query(FileEntity)
            .options(joinedload(FileEntity.tags))  # 태그를 조인해서 로드
            .filter(
                # 모든 태그를 포함하는지 확인
                and_(*[
                    FileEntity.tags.any(FileTagEntity.tag == tag) for tag in tags
                ])
            )
            .order_by(FileEntity.created_at.desc())
            .limit(1)
            .all()
        )


class LLMRepository(SqlAlchemyBaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, LLMQAEntity)

    def find_prompt_by_user_id(self, user_id: str) -> list[Type[LLMPromptEntity]]:
        return (
            self.session.query(LLMPromptEntity)
            .filter(LLMPromptEntity.user_id == user_id)
            .order_by(LLMPromptEntity.created_at.desc())
            .limit(1)
            .all()
        )
