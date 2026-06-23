import ollama
import config

# Keep conversation history so Friday remembers context within a session
conversation_history = [
    {"role": "system", "content": config.SYSTEM_PROMPT}
]


def ask_friday(user_text):
    conversation_history.append({"role": "user", "content": user_text})

    response = ollama.chat(
        model=config.LLM_MODEL,
        messages=conversation_history,
        options={
            "num_ctx": 2048,      # smaller context window = less RAM
            "num_thread": 3       # leave 1 core free for STT/TTS/Windows
        }
    )

    reply = response['message']['content']
    conversation_history.append({"role": "assistant", "content": reply})

    return reply