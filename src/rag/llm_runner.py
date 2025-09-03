# src/rag/llm_runner.py
import ollama

MODEL_NAME = "gemma3:4b"

def call_ollama(prompt: str, system_prompt: str | None = None) -> str:
    """
    Gemma-4B modelinden yanıt alır.

    Args:
        prompt (str): Kullanıcı + context prompt’u
        system_prompt (str | None): İsteğe bağlı sistem komutu

    Returns:
        str: Model yanıtı
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = ollama.chat(model=MODEL_NAME, messages=messages)
    return response["message"]["content"].strip()
