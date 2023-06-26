import os

from azure.storage.blob import BlobServiceClient

CONNECT_STR = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("AZURE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)


def upload_blob(path, buf):
    container_client.upload_blob(name=path, data=buf.getvalue())


def append_file_to_blob(path):
    with open(path, mode="rb") as data:
        container_client.upload_blob(name=path, data=data, blob_type="AppendBlob")
