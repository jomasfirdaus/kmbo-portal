import io
from datetime import timedelta

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from minio import Minio
from minio.error import S3Error


@deconstructible
class MinioMediaStorage(Storage):
    """Django Storage backend backed by a MinIO bucket via the official minio SDK."""

    def __init__(self):
        self.bucket_name = settings.MINIO_BUCKET_NAME
        # Minio() expects a bare host[:port], not a scheme-prefixed URL.
        self.endpoint = settings.MINIO_ENDPOINT.split('://', 1)[-1].rstrip('/')
        self.use_ssl = settings.MINIO_USE_SSL
        self.url_expiry = timedelta(seconds=settings.MINIO_URL_EXPIRY_SECONDS)
        self.client = Minio(
            self.endpoint,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=self.use_ssl,
        )

    @staticmethod
    def _normalize_name(name):
        return name.replace('\\', '/').lstrip('/')

    def _open(self, name, mode='rb'):
        name = self._normalize_name(name)
        response = self.client.get_object(self.bucket_name, name)
        try:
            data = response.read()
        finally:
            response.close()
            response.release_conn()
        return File(io.BytesIO(data), name=name)

    def _save(self, name, content):
        name = self._normalize_name(name)
        content.seek(0)
        data = content.read()
        content_type = getattr(content, 'content_type', None) or 'application/octet-stream'
        self.client.put_object(
            self.bucket_name,
            name,
            io.BytesIO(data),
            length=len(data),
            content_type=content_type,
        )
        return name

    def exists(self, name):
        name = self._normalize_name(name)
        try:
            self.client.stat_object(self.bucket_name, name)
            return True
        except S3Error as exc:
            if exc.code in ('NoSuchKey', 'NoSuchObject'):
                return False
            raise

    def delete(self, name):
        name = self._normalize_name(name)
        self.client.remove_object(self.bucket_name, name)

    def size(self, name):
        name = self._normalize_name(name)
        return self.client.stat_object(self.bucket_name, name).size

    def url(self, name):
        name = self._normalize_name(name)
        return self.client.presigned_get_object(
            self.bucket_name, name, expires=self.url_expiry,
        )

    def listdir(self, path):
        path = self._normalize_name(path)
        prefix = path if not path or path.endswith('/') else f'{path}/'
        directories, files = set(), []
        for obj in self.client.list_objects(self.bucket_name, prefix=prefix, recursive=False):
            relative = obj.object_name[len(prefix):]
            if obj.is_dir:
                directories.add(relative.rstrip('/'))
            else:
                files.append(relative)
        return list(directories), files
