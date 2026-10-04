"""
Local Llama Chat — a 100% local ChatGPT alternative.

Powered by Llama 3.2 Vision served through Ollama. Chat with text,
attach images and ask questions about them. No API keys, no cloud,
your data never leaves your machine.

Replies stream token-by-token as the model generates them.

Setup:
    1. Install Ollama: https://ollama.com  (or `curl -fsSL https://ollama.com/install.sh | sh`)
    2. Pull the model:  ollama pull llama3.2-vision
    3. Install deps:    pip install -r requirements.txt
    4. Run:             chainlit run app.py -w

Environment:
    LLAMA_MODEL   Model to use (default: llama3.2-vision)
    SYSTEM_PROMPT System prompt override
"""

import os

import chainlit as cl
import ollama

MODEL = os.getenv("LLAMA_MODEL", "llama3.2-vision")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful assistant running 100% locally on the user's machine.",
)

WELCOME_MESSAGE = (
    f"Hello! I'm your fully local ChatGPT alternative, running on {MODEL}. "
    "Ask me anything — you can also attach an image and ask about it. "
    "How can I help you today?"
)

OLLAMA_DOWN_HINT = (
    "I couldn't reach Ollama. Make sure it's running and the model is pulled:\n\n"
    "```bash\n"
    "ollama serve\n"
    f"ollama pull {MODEL}\n"
    "```"
)


@cl.on_chat_start
async def start_chat():
    """Initialise a fresh conversation with a system prompt."""
    cl.user_session.set(
        "interaction",
        [{"role": "system", "content": SYSTEM_PROMPT}],
    )

    msg = cl.Message(content="")
    for token in WELCOME_MESSAGE:
        await msg.stream_token(token)
    await msg.send()


@cl.on_message
async def main(message: cl.Message):
    """Handle an incoming message, streaming the reply as it's generated."""
    images = [f for f in message.elements if "image" in f.mime]

    interaction = cl.user_session.get("interaction")
    user_turn: dict = {"role": "user", "content": message.content}
    if images:
        user_turn["images"] = [f.path for f in images]
    interaction.append(user_turn)

    msg = cl.Message(content="")

    try:
        # Note: with stream=True the request is lazy — errors surface
        # while iterating, so the whole loop lives inside the try.
        stream = ollama.chat(model=MODEL, messages=interaction, stream=True)
        reply_parts: list[str] = []
        for chunk in stream:
            token = chunk.message.content or ""
            reply_parts.append(token)
            await msg.stream_token(token)
    except Exception:
        # Don't poison the history with the failed turn; surface a fix-it hint.
        interaction.pop()
        await msg.stream_token(OLLAMA_DOWN_HINT)
        await msg.send()
        return

    interaction.append({"role": "assistant", "content": "".join(reply_parts)})
    await msg.send()
