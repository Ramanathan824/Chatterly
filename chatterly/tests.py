from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase

from .views import get_gemini_client


class ChatResponseTests(TestCase):
    @patch("chatterly.views.get_gemini_client")
    def test_chat_response_streams_generated_text(self, get_client):
        client = get_client.return_value
        client.models.generate_content_stream.return_value = [
            SimpleNamespace(text="Hello"),
            SimpleNamespace(text=" there!"),
        ]

        response = self.client.post("/chat/", {"message": "Hi"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)
        self.assertEqual(
            b"".join(response.streaming_content),
            b"Hello there!",
        )

    @patch("chatterly.views.genai.Client")
    def test_gemini_client_is_cached_with_bounded_request_time(self, client_class):
        get_gemini_client.cache_clear()
        self.addCleanup(get_gemini_client.cache_clear)

        first_client = get_gemini_client("test-api-key")
        second_client = get_gemini_client("test-api-key")

        self.assertIs(first_client, second_client)
        client_class.assert_called_once()
        options = client_class.call_args.kwargs["http_options"]
        self.assertEqual(options.timeout, 20_000)
        self.assertEqual(options.retry_options.attempts, 1)
