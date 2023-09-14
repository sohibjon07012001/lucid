import typing

from azure.storage.blob import BlobServiceClient, ContentSettings
from config import AzureStorage

FileURL = str


async def upload_file(file: typing.BinaryIO, file_name: str, file_type: str) -> typing.Optional[FileURL]:
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(AzureStorage.CONNECTION_STR)
    blob_client = blob_service_client.get_blob_client(container='lucid',
                                                      blob=file_name)
    cnt_settings = ContentSettings(content_type=file_type)

    if blob_client.exists():
        blob_client.delete_blob(delete_snapshots='include')

    blob_client.upload_blob(file, content_settings=cnt_settings)
    return blob_client.url