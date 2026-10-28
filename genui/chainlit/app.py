import asyncio
import os
from collections.abc import Sequence
from urllib.parse import urlsplit

import chainlit as cl
import httpx
import psycopg2
from openai import AsyncOpenAI
from pgvector.psycopg2 import register_vector
from psycopg2.extensions import connection as PgConnection

OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "http://ollama-gateway:11435/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
PGVECTOR_URL = os.getenv("PGVECTOR_URL")


def validate_public_url(value: str) -> str:
    """Accept only browser-safe HTTP(S) URLs for the OpenUI link."""
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("OPENUI_PUBLIC_URL must be an absolute HTTP(S) URL")
    return value


OPENUI_PUBLIC_URL = validate_public_url(
    os.getenv("OPENUI_PUBLIC_URL", "http://localhost:3001")
)

client = AsyncOpenAI(base_url=OLLAMA_ENDPOINT, api_key="ollama")


def get_db() -> PgConnection:
    """Create a pgvector-enabled database connection."""
    if not PGVECTOR_URL:
        raise RuntimeError("PGVECTOR_URL is required")

    connection = psycopg2.connect(PGVECTOR_URL)
    register_vector(connection)
    return connection


def query_runbooks(embedding: Sequence[float]) -> str:
    """Query the two runbooks closest to the supplied embedding."""
    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
        SELECT title, service, content, 1 - (embedding <=> %s) AS similarity
        FROM operational_runbooks
        ORDER BY embedding <=> %s
        LIMIT 2;
        """,
                (list(embedding), list(embedding)),
            )
            rows = cursor.fetchall()
    finally:
        connection.close()

    if not rows:
        return "No matching runbooks in pgvector."

    return "\n\n".join(
        f"### {title} ({service})\n{content}\nSimilarity: {similarity:.3f}"
        for title, service, content, similarity in rows
    )


async def search_pgvector(prompt: str) -> str:
    """Retrieve operational runbooks using cosine distance."""
    try:
        embedding_url = f"{OLLAMA_ENDPOINT.removesuffix('/v1')}/api/embeddings"
        async with httpx.AsyncClient(timeout=10.0) as http:
            response = await http.post(
                embedding_url,
                json={"model": EMBEDDING_MODEL, "prompt": prompt},
            )
            response.raise_for_status()
            embedding = response.json().get("embedding")

        if not embedding:
            return "No contextual runbooks found."

        return await asyncio.to_thread(query_runbooks, embedding)
    except (httpx.HTTPError, psycopg2.Error, RuntimeError, ValueError) as error:
        return f"Runbook retrieval unavailable: {error}"


@cl.on_chat_start
async def on_chat_start() -> None:
    await cl.Message(
        content=(
            "### Generative UI Observability Copilot\n"
            "Connected to **Host Ollama**, **pgvector RAG**, and **OpenUI**.\n"
            "Ask a monitoring question or request an interactive remediation widget."
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    async with cl.Step(name="Vector Retrieval (pgvector)") as step:
        context = await search_pgvector(message.content)
        step.output = f"Retrieved context:\n{context[:300]}..."

    system_prompt = (
        "You are an SRE copilot with Generative UI capabilities. "
        "Use the supplied operational runbooks as evidence. "
        "Never claim that an action was executed unless a tool result confirms it.\n\n"
        f"KNOWLEDGE BASE CONTEXT:\n{context}\n\n"
        "When proposing dynamic forms, buttons, or dashboards, describe the intended "
        "OpenUI component and require operator confirmation for disruptive actions."
    )

    response_message = cl.Message(content="")
    await response_message.send()

    stream = await client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message.content},
        ],
        stream=True,
    )

    full_text = ""
    async for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        full_text += token
        await response_message.stream_token(token)

    await response_message.update()

    if any(
        keyword in full_text.lower()
        for keyword in ("widget", "card", "component", "button", "openui")
    ):
        await cl.Message(
            content=(
                "Interactive UI component available in the OpenUI surface: "
                f"<{OPENUI_PUBLIC_URL}>"
            ),
        ).send()
