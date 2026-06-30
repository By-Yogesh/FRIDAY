import ollama
import config

conversation_history = [
    {"role": "system", "content": config.SYSTEM_PROMPT}
]


def ask_friday(user_text):
    conversation_history.append({"role": "user", "content": user_text})

    response = ollama.chat(
        model=config.LLM_MODEL,
        messages=conversation_history,
        options={
            "num_ctx": config.LLM_NUM_CTX,
            "num_thread": config.LLM_NUM_THREAD
        }
    )

    reply = response['message']['content']
    conversation_history.append({"role": "assistant", "content": reply})
    return reply


def ask_friday_stream(user_text):
    """Streams reply token by token. Yields each token as it arrives."""
    conversation_history.append({"role": "user", "content": user_text})

    stream = ollama.chat(
        model=config.LLM_MODEL,
        messages=conversation_history,
        stream=True,
        options={
            "num_ctx": config.LLM_NUM_CTX,
            "num_thread": config.LLM_NUM_THREAD
        }
    )

    full_reply = ""
    for chunk in stream:
        token = chunk['message']['content']
        full_reply += token
        yield token

    conversation_history.append({"role": "assistant", "content": full_reply})