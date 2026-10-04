# Local Llama Chat 🦙💬

A **100% local ChatGPT alternative** powered by Llama 3.2 Vision, served through
[Ollama](https://ollama.com) with a [Chainlit](https://chainlit.io) chat UI.

- 💬 Chat with streaming responses, ChatGPT-style
- 🖼️ Attach images and ask questions about them (multimodal)
- 🔒 No API keys, no cloud, no tracking — everything runs on your machine

Built as project #1 of my AI engineering journey, following the
[AI Engineering Hub](https://github.com/patchy631/ai-engineering-hub) roadmap.

## Quickstart

**1. Install Ollama** → https://ollama.com/download

**2. Pull the model**
```bash
ollama pull llama3.2-vision
```

**3. Install Python dependencies** (Python 3.11+)
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
chainlit run app.py -w
```
Then open http://localhost:8000 in your browser.

## Configuration

| Variable        | Default                                              | What it does              |
|-----------------|------------------------------------------------------|---------------------------|
| `LLAMA_MODEL`   | `llama3.2-vision`                                    | Ollama model to chat with |
| `SYSTEM_PROMPT` | `You are a helpful assistant running 100% locally…` | System prompt override    |

Example:
```bash
LLAMA_MODEL=llama3.2 chainlit run app.py -w
```

## How it works

```
You ──text / image──▶ Chainlit UI ──▶ Ollama (llama3.2-vision) ──▶ streaming reply
                              ▲
                     conversation history kept
                     in the user session
```

Each chat turn (plus any attached image paths) is appended to the session
history and sent to `ollama.chat`. Replies stream back token-by-token,
typewriter style. If Ollama isn't reachable, the app tells you how to fix it
instead of crashing.

## Project structure

```
├── app.py            # Chainlit app: chat handlers, Ollama calls, streaming
├── requirements.txt  # chainlit, ollama, pydantic (pinned for compatibility)
└── README.md
```

## Roadmap

This is the first build in a series working through AI engineering —
next up: local RAG over my own documents, then AI agents.
