from src.app.dto.user_dto import CreatedUser, GrantedUser
from src.domain.model import UserEntity, UserGrantEnum
from src.infra.encryption import BCrypt
from src.uow import SqlAlchemyUow


class UserUseCase:
    def __init__(self, uow: SqlAlchemyUow):
        self.uow = uow
        self.bcrypt = BCrypt()

    def create_user(self, user_id: str, password: str) -> CreatedUser:
        with self.uow:
            found_user = self.uow.users.get(user_id)
            if found_user:
                raise RuntimeError(f'이미 존재하는 계정')

            hashed_password = self.bcrypt.hash_password(password)
            new_user = UserEntity(
                id=user_id,
                password=hashed_password,
            )
            self.uow.users.add(new_user)
            self.uow.commit()
            return CreatedUser.of(new_user)

    def grant_user(self, user_id: str, grant_str: str) -> GrantedUser:

        with self.uow:
            grant_enum = UserGrantEnum(grant_str)
            found_user = self.uow.users.find_by_id(user_id=user_id)
            if not found_user:
                raise RuntimeError(f'존재 하지 않는 계정입니다.')
            found_user.add_grant(grant_enum)
            self.uow.users.add(found_user)
            self.uow.commit()
            return GrantedUser(
                user_id=user_id,
                grant=grant_enum,
            )
