from enum import Enum

from sqlalchemy import Column, String, func, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.infra.db import StringifiedEnum, BaseEntity, BaseTable


## user ################################################################################################################
class UserEntity(BaseTable):
    __tablename__ = "user"

    id: str = Column(String, primary_key=True)
    password: str = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    grants = relationship("UserGrantEntity", back_populates="user", cascade="all, delete-orphan")


class UserGrantEnum(str, Enum):
    USE_CHAT_BOT = 'use_chat_bot'


class UserGrantEntity(BaseTable):
    __tablename__ = "user_grant"

    id: str = Column(StringifiedEnum(UserGrantEnum), primary_key=True)  # 권한 고유 ID
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)  # UserEntity와 연결
    # UserEntity와의 관계 설정
    user = relationship("UserEntity", back_populates="grants")


## file ################################################################################################################
class FileStatusEnum(str, Enum):
    SYNC = 'sync'
    UNSYNC = "unsync"
    REMOVE = 'remove'


class FileExtEnum(str, Enum):
    PNG = 'png'
    JPEG = 'jpeg'


class FileStorageEnum(str, Enum):
    LOCAL = 'local'
    S3 = "s3"


class FileEntity(BaseTable):
    __tablename__ = 'file'

    id = Column(String(256), primary_key=True, unique=True, nullable=False, comment="파일 자체의 해시 값")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    origin_name = Column(String, nullable=False)

    status = Column(
        StringifiedEnum(FileStatusEnum),
        default=FileStatusEnum.UNSYNC,
        nullable=False
    )

    ext = Column(
        StringifiedEnum(FileExtEnum),
        default=FileExtEnum.PNG,
        nullable=False
    )

    save_dir = Column(String, nullable=False)

    storage = Column(
        StringifiedEnum(FileStorageEnum),
        default=FileStorageEnum.LOCAL,
        nullable=False
    )

    url = Column(String, nullable=False)

    # UserEntity와의 관계 설정
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("UserEntity")

    def is_ext(self, ext: FileExtEnum) -> bool:
        if self.ext == ext:
            return True
        return False

    def get_stored_file_name(self) -> str:
        # 현재 저장된 파일에 이름 -> 원본 이름과 다르다.
        return f"{self.id}.{self.ext}"