from src.domain.model import UserGrantEnum
from src.uow import SqlAlchemyUow


class AuthUseCase:
    def __init__(self, uow: SqlAlchemyUow):
        self.uow = uow

    def check_admin(self, user_id: str):
        with self.uow:
            found_user = self.uow.users.get(pk=user_id)
            if found_user is None:
                raise RuntimeError(f'해당 유저를 찾지 못했습니다.')
            if not found_user.check_admin():
                raise RuntimeError(f'해당 유저를 관리자 권한이 없습니다.')

    def check_grant(self, user_id: str, grant_enum: UserGrantEnum):
        with self.uow:
            found_user = self.uow.users.find_by_id(user_id=user_id)
            if found_user is None:
                raise RuntimeError(f'해당 유저를 찾지 못했습니다.')
            if not found_user.check_grant(grant_enum):
                raise RuntimeError(f'해당 접근 권한 없습니다: {grant_enum.get_ko_str()}')
