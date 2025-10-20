"""Sample script to call Azure OpenAI using the Responses API and DefaultAzureCredential."""

from __future__ import annotations

import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI

_SCOPE = "https://cognitiveservices.azure.com/.default"


def _get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"Set the {name} environment variable.")
    return value


def _build_base_url(endpoint: str) -> str:
    endpoint = endpoint.rstrip("/")
    return f"{endpoint}/openai/v1/"


def main() -> None:
    """Resolve configuration, send a test prompt, and print the JSON response."""
    load_dotenv()

    endpoint = _get_required_env("AZURE_OPENAI_ENDPOINT")
    deployment = _get_required_env("AZURE_OPENAI_DEPLOYMENT")
    prompt = os.environ.get(
        "AZURE_OPENAI_TEST_PROMPT",
        "Peux-tu me donner une courte blague en français sur les nuages ?",
    )

    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_provider = get_bearer_token_provider(credential, _SCOPE)

    client = OpenAI(base_url=_build_base_url(endpoint), api_key=token_provider)

    response = client.responses.create(model=deployment, input=prompt)
    print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
