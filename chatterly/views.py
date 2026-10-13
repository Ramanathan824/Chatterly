import time
from functools import lru_cache

from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from google import genai
from google.genai import types


@lru_cache(maxsize=1)
def get_gemini_client(api_key):
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=20_000,
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )


def home(request):
    return render(request, "index.html")


def chat_response(request):
    total_start = time.perf_counter()

    if request.method != "POST":
        return JsonResponse(
            {"response": "Invalid request"},
            status=405
        )

    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse({
            "response": "Please type a message!"
        })

    api_key = settings.GEMINI_API_KEY

    if not api_key:
        return JsonResponse({
            "response": "AI configuration error. Please try again later."
        }, status=500)

    try:
        client_start = time.perf_counter()
        client = get_gemini_client(api_key)
        client_time = time.perf_counter() - client_start
        print(f"Client initialization: {client_time:.2f}s")

    except Exception as error:
        print("GEMINI API ERROR:", repr(error))
        print(
            f"Failed request total time: "
            f"{time.perf_counter() - total_start:.2f}s"
        )

        return JsonResponse({
            "response": (
                "Sorry, Chatterly couldn't connect to AI right now. "
                "Please try again."
            )
        }, status=502)

    def stream_response():
        api_start = time.perf_counter()
        first_text_time = None

        try:
            for chunk in client.models.generate_content_stream(
                model="gemini-3.1-flash-lite",
                contents=(
                    "You are Chatterly, a friendly AI assistant. "
                    "Answer clearly and concisely.\n\n"
                    f"User: {message}"
                ),
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_level="MINIMAL"
                    ),
                    max_output_tokens=512,
                ),
            ):
                text = chunk.text
                if text:
                    if first_text_time is None:
                        first_text_time = time.perf_counter() - api_start
                        print(
                            f"Gemini time to first text: "
                            f"{first_text_time:.2f}s"
                        )
                    yield text

            if first_text_time is None:
                yield "I couldn't generate a response. Please try again."
        except Exception as error:
            print("GEMINI API ERROR:", repr(error))
            yield (
                "\nSorry, Chatterly couldn't connect to AI right now. "
                "Please try again."
            )
        finally:
            print(
                f"Gemini API time: {time.perf_counter() - api_start:.2f}s"
            )
            print(
                f"Total backend time: "
                f"{time.perf_counter() - total_start:.2f}s"
            )

    response = StreamingHttpResponse(
        stream_response(),
        content_type="text/plain; charset=utf-8",
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
