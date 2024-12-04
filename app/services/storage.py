import os
from pathlib import Path
import uuid
from abc import ABC, abstractmethod

from fastapi import UploadFile
from azure.storage.blob import BlobServiceClient

class StorageProvider(ABC):
    @abstractmethod
    async def save_file(self, file: UploadFile) -> str:
        """Save a file and return its public URL"""
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage"""
        raise NotImplementedError

class LocalStorage(StorageProvider):
    def __init__(self, base_path: str, base_url: str):
        self.base_path = base_path
        self.base_url = base_url
        os.makedirs(base_path, exist_ok=True)

    async def save_file(self, file: UploadFile) -> str:
        if file.filename is not None:
            ext = Path(file.filename).suffix
        else:
            ext = ""
        unique_filename = f"{uuid.uuid4()}{ext}"

        file_path = os.path.join(self.base_path, unique_filename)
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        return f"{self.base_url}/{unique_filename}"

    async def delete_file(self, file_path: str) -> bool:
        full_path = os.path.join(self.base_path, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

class AzureBlobStorage(StorageProvider):
    def __init__(self, connection_string: str, container_name: str):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    async def save_file(self, file: UploadFile) -> str:
        if file.filename is not None:
            ext = Path(file.filename).suffix
        else:
            ext = ""
        unique_filename = f"{uuid.uuid4()}{ext}"

        blob_client = self.container_client.get_blob_client(unique_filename)
        content = await file.read()
        blob_client.upload_blob(content, overwrite=True)
        return blob_client.url

    async def delete_file(self, file_path: str) -> bool:
        blob_client = self.container_client.get_blob_client(file_path)
        try:
            blob_client.delete_blob()
            return True
        except Exception as e:
            # There is no BlobNotFound exception in the Azure SDK
            if "BlobNotFound" in str(e):
                return False
            raise e

def get_storage_provider() -> StorageProvider:
    if os.getenv("ENVIRONMENT") == "production":
        return AzureBlobStorage(
            connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING") or "",
            container_name=os.getenv("AZURE_STORAGE_CONTAINER_NAME") or ""
        )
    else:
        return LocalStorage(
            base_path="static/medias",
            base_url="http://127.0.0.1:8000/static/medias"
        )
