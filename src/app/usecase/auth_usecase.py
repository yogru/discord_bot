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
