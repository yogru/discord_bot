from enum import Enum
from typing import Optional

from sqlalchemy import Column, String, func, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.infra.db import StringifiedEnum, BaseEntity, BaseTable


## user ################################################################################################################

class UserKindEnum(str, Enum):
    ADMIN = 'admin'
    CLIENT = 'client'


class UserGrantEnum(str, Enum):
    USE_CHAT_BOT = 'use_chat_bot'


class UserEntity(BaseTable):
    __tablename__ = "user_entity"

    id: str = Column(String, primary_key=True)
    password: str = Column(String, nullable=False)
    kind: UserKindEnum = Column(StringifiedEnum(UserKindEnum), nullable=False, default=UserKindEnum.CLIENT)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    grants = relationship("UserGrantEntity", back_populates="user", cascade="all, delete-orphan")

    def check_admin(self):
        if self.kind == UserKindEnum.ADMIN:
            return True
        return False

    def find_grant(self, grant_enum: UserGrantEnum) -> Optional['UserGrantEntity']:
        for grant in self.grants:
            if grant.equal_enum(grant_enum):
                return grant
        return None

    def add_grant(self, grant_enum: UserGrantEnum) -> 'UserGrantEntity':
        found_grant = self.find_grant(grant_enum)
        if found_grant:
            raise RuntimeError("이미 존재 하는 권한 입니다.")
        new_grant = UserGrantEntity(
            grant=grant_enum,
            user_id=self.id
        )
        self.grants.append(new_grant)
        return new_grant


class UserGrantEntity(BaseEntity):
    __tablename__ = "user_grant"

    grant: str = Column(StringifiedEnum(UserGrantEnum), primary_key=True)  # 권한 고유 ID
    user_id = Column(String, ForeignKey("user_entity.id", ondelete="CASCADE"), nullable=False)  # UserEntity와 연결
    # UserEntity와의 관계 설정
    user = relationship("UserEntity", back_populates="grants")

    def equal_enum(self, grant_enum: UserGrantEnum):
        return self.grant == grant_enum


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
    user_id = Column(String, ForeignKey("user_entity.id", ondelete="CASCADE"), nullable=False)
    user = relationship("UserEntity")

    def is_ext(self, ext: FileExtEnum) -> bool:
        if self.ext == ext:
            return True
        return False

    def get_stored_file_name(self) -> str:
        # 현재 저장된 파일에 이름 -> 원본 이름과 다르다.
        return f"{self.id}.{self.ext}"
