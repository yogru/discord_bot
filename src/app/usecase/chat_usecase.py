from src.infra.db import AbstractUnitOfWork


class ChatUseCase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

