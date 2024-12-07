from pydantic import BaseModel

from src.domain.model import UserEntity, UserGrantEnum


class CreatedUser(BaseModel):
    user_id: str

    @staticmethod
    def of(entity: UserEntity) -> 'CreatedUser':
        return CreatedUser(
            user_id=entity.id
        )


class GrantedUser(BaseModel):
    user_id: str
    grant: UserGrantEnum
