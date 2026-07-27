from unittest.mock import MagicMock, patch

from django.core.files.base import ContentFile
from django.test import SimpleTestCase, override_settings

from minio.error import S3Error

from kmbo.storage import MinioMediaStorage


@override_settings(
    MINIO_ENDPOINT='minio.example.com',
    MINIO_ACCESS_KEY='test-access-key',
    MINIO_SECRET_KEY='test-secret-key',
    MINIO_BUCKET_NAME='test-bucket',
    MINIO_USE_SSL=True,
    MINIO_URL_EXPIRY_SECONDS=3600,
)
class MinioMediaStorageTests(SimpleTestCase):
    """Exercises MinioMediaStorage against a mocked minio.Minio client (no network calls)."""

    def setUp(self):
        patcher = patch('kmbo.storage.Minio')
        self.addCleanup(patcher.stop)
        mock_minio_cls = patcher.start()
        self.mock_client = MagicMock()
        mock_minio_cls.return_value = self.mock_client
        self.mock_minio_cls = mock_minio_cls
        self.storage = MinioMediaStorage()

    def test_client_configured_from_settings(self):
        self.mock_minio_cls.assert_called_once_with(
            'minio.example.com',
            access_key='test-access-key',
            secret_key='test-secret-key',
            secure=True,
        )

    def test_endpoint_scheme_is_stripped(self):
        with override_settings(MINIO_ENDPOINT='https://minio.example.com'):
            MinioMediaStorage()
        self.mock_minio_cls.assert_called_with(
            'minio.example.com',
            access_key='test-access-key',
            secret_key='test-secret-key',
            secure=True,
        )

    def test_save_uploads_content_and_returns_name(self):
        name = self.storage._save('geleri/photo.jpg', ContentFile(b'binary-data'))

        self.assertEqual(name, 'geleri/photo.jpg')
        self.mock_client.put_object.assert_called_once()
        args, kwargs = self.mock_client.put_object.call_args
        self.assertEqual(args[0], 'test-bucket')
        self.assertEqual(args[1], 'geleri/photo.jpg')
        self.assertEqual(kwargs['length'], len(b'binary-data'))

    def test_open_reads_bytes_from_bucket(self):
        response = MagicMock()
        response.read.return_value = b'file-content'
        self.mock_client.get_object.return_value = response

        result = self.storage._open('geleri/photo.jpg')

        self.mock_client.get_object.assert_called_once_with('test-bucket', 'geleri/photo.jpg')
        self.assertEqual(result.read(), b'file-content')
        response.close.assert_called_once()
        response.release_conn.assert_called_once()

    def test_exists_true_when_stat_succeeds(self):
        self.mock_client.stat_object.return_value = MagicMock()
        self.assertTrue(self.storage.exists('geleri/photo.jpg'))

    def test_exists_false_on_no_such_key(self):
        self.mock_client.stat_object.side_effect = S3Error(
            response=MagicMock(), code='NoSuchKey', message='not found',
            resource='/test-bucket/geleri/photo.jpg', request_id='req-id', host_id='host-id',
            bucket_name='test-bucket', object_name='geleri/photo.jpg',
        )
        self.assertFalse(self.storage.exists('geleri/photo.jpg'))

    def test_exists_reraises_other_s3_errors(self):
        self.mock_client.stat_object.side_effect = S3Error(
            response=MagicMock(), code='AccessDenied', message='denied',
            resource='/test-bucket/geleri/photo.jpg', request_id='req-id', host_id='host-id',
            bucket_name='test-bucket', object_name='geleri/photo.jpg',
        )
        with self.assertRaises(S3Error):
            self.storage.exists('geleri/photo.jpg')

    def test_delete_removes_object(self):
        self.storage.delete('geleri/photo.jpg')
        self.mock_client.remove_object.assert_called_once_with('test-bucket', 'geleri/photo.jpg')

    def test_size_returns_stat_size(self):
        self.mock_client.stat_object.return_value = MagicMock(size=1234)
        self.assertEqual(self.storage.size('geleri/photo.jpg'), 1234)

    def test_url_returns_presigned_url(self):
        self.mock_client.presigned_get_object.return_value = 'https://minio.example.com/signed-url'

        url = self.storage.url('geleri/photo.jpg')

        self.assertEqual(url, 'https://minio.example.com/signed-url')
        self.mock_client.presigned_get_object.assert_called_once_with(
            'test-bucket', 'geleri/photo.jpg', expires=self.storage.url_expiry,
        )

    def test_name_normalization_strips_leading_slash_and_backslashes(self):
        self.storage.delete('/geleri\\photo.jpg')
        self.mock_client.remove_object.assert_called_once_with('test-bucket', 'geleri/photo.jpg')
