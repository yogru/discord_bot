from minio import Minio

from src.infra.env import EnvSettings


class MinIoWrapper:
    def __init__(self, env: EnvSettings):
        self.env = env
        self.client = None

    def init(self):
        self.client = Minio(
            self.env.OS_URL,  # MinIO 서버 URL
            access_key=self.env.OS_ACCESS_KEY,  # MinIO 액세스 키
            secret_key=self.env.OS_SECRET_KEY,  # MinIO 시크릿 키
            secure=self.env.OS_SECURE  # HTTPS를 사용하지 않을 경우 False
        )

    def upload(self, upload_name: str, local_file_path: str):
        try:
            self.client.fput_object(
                "img",  # 버킷 이름
                upload_name,  # MinIO에 저장될 파일 이름
                local_file_path  # 로컬 파일 경로
            )
            print("File uploaded successfully.")
        except Exception as e:
            print(f"Error uploading file: {e}")
