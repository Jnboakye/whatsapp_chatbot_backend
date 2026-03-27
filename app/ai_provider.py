from typing import List
from app.config import get_settings
from app.prompt import SYSTEM_PROMPT

settings = get_settings()


async def get_ai_response(history: List[dict]) -> str:
    """
    Route to the correct AI provider based on settings.ai_provider.
    Accepts full conversation history and returns the assistant's reply.
    """
    provider = settings.ai_provider.lower()

    if provider == "claude":
        return await _call_claude(history)
    elif provider == "openai":
        return await _call_openai(history)
    else:
        raise ValueError(f"Unknown AI provider: '{provider}'. Use 'claude' or 'openai'.")


# ─── Claude (Anthropic) ───────────────────────────────────────────────────────

async def _call_claude(history: List[dict]) -> str:
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    response = await client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    return response.content[0].text


# ─── OpenAI ───────────────────────────────────────────────────────────────────

async def _call_openai(history: List[dict]) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content