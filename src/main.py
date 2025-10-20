"""Sample script to call Azure OpenAI GPT-4o using DefaultAzureCredential."""

from __future__ import annotations

import os
from typing import Iterable

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    ChatCompletionsRequest,
    SystemMessage,
    TextContentItem,
    UserMessage,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def create_client() -> ChatCompletionsClient:
    """Instantiate a chat client using the DefaultAzureCredential."""
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    if not endpoint:
        raise ValueError("Set the AZURE_OPENAI_ENDPOINT environment variable.")

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    return ChatCompletionsClient(endpoint=endpoint, credential=credential)


def build_request() -> ChatCompletionsRequest:
    """Build the chat completion request payload."""
    model = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
    if not model:
        raise ValueError("Set the AZURE_OPENAI_DEPLOYMENT environment variable.")

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        UserMessage(content="Donne moi une blague courte en français sur les nuages."),
    ]

    return ChatCompletionsRequest(model=model, messages=messages, temperature=0.7)


def extract_text(content: Iterable[TextContentItem]) -> str:
    """Flatten the list of content blocks returned by the API."""
    parts: list[str] = []
    for block in content:
        if isinstance(block, TextContentItem):
            parts.append(block.text)
    return "\n".join(parts)


def main() -> None:
    """Load configuration, send a test prompt, and print the response."""
    load_dotenv()

    client = create_client()
    request = build_request()

    response = client.complete(request)

    choice = response.choices[0]
    print("Assistant:")
    print(extract_text(choice.message.content))


if __name__ == "__main__":
    main()
