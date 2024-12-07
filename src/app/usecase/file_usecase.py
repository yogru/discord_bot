import uuid
from typing import List

from src.domain.model import FileEntity, FileStorageEnum, FileStatusEnum
from src.infra.object_storage import MinIoWrapper
from src.uow import SqlAlchemyUow


class FileUseCase:
    def __init__(self,
                 uow: SqlAlchemyUow,
                 min_io: MinIoWrapper
                 ):
        self.uow = uow
        self.min_io = min_io

    def upload_file(self,
                    user_id: str,
                    filename: str,
                    saved_path: str,
                    tags: List[str],
                    storage: FileStorageEnum = FileStorageEnum.MIN_IO,
                    url: str = None
                    ):
        file_id = str(uuid.uuid4())
        ext = filename.split('.')[-1]
        upload_name = f"{file_id}.{ext}"
        self.min_io.upload(
            upload_name=upload_name,
            local_file_path=saved_path
        )
        with self.uow:
            if url is None:
                url = self.min_io.get_public_url(upload_name)
            new_file_entity = FileEntity(
                id=file_id,
                origin_name=filename,
                url=url,
                user_id=user_id,
                storage=storage,
                status=FileStatusEnum.SYNC
            )
            new_file_entity.add_tags(tags)
            self.uow.files.add(new_file_entity)
            self.uow.commit()

    def get_url(self, tags: List[str]) -> List[str]:
        with self.uow:
            files = self.uow.files.find_by_tags(tags=tags)
            return [f.url for f in files]
