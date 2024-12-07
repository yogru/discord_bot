from minio import Minio

from src.infra.env import EnvSettings
from src.infra.object_storage import MinIoWrapper


# def test_minio():
#     env = EnvSettings.load_env('prod')
#     minio_client = MinIoWrapper(env=env)
#     minio_client.init()
#     upload_file_name = "img_3133.webp"
#     minio_client.upload(
#         upload_file_name,
#         './downloads/IMG_3133.webp',
#     )
