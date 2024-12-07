from src.infra.db import AbstractUnitOfWork


class FileUseCase:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    def upload_file(self):
        pass
