
# PocketAgent - Day 8
# AI assistant that runs on your laptop. No internet. No API key.
# Model: qwen2.5:3b (or whatever you have in ollama)

import ollama
import sys
import time

MODEL = "qwen2.5:3b"

SYSTEM_PROMPT = """You are PocketAgent, a helpful AI assistant 
running entirely on the user's laptop with no internet.
Be short, direct, and useful and a little dirty-minded, and funny:)."""

# this list stores the whole conversation
# so the AI remembers what was said before
conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


def ask(user_message):
    # add what the user said to memory
    conversation.append({
        "role": "user",
        "content": user_message
    })

    full_response = ""

    print("PocketAgent: ", end="", flush=True)

    # stream the response word by word
    stream = ollama.chat(
        model=MODEL,
        messages=conversation,
        stream=True
    )

    for chunk in stream:
        word = chunk["message"]["content"]
        print(word, end="", flush=True)
        full_response += word

    print()

    # add the response to memory too
    conversation.append({
        "role": "assistant",
        "content": full_response
    })


def clear_memory():
    global conversation
    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Memory cleared.\n")


def main():
    print("\n--- PocketAgent ---")
    print(f"Model: {MODEL}")
    print("No internet. Runs locally.")
    print("Commands: 'clear' = reset memory | 'exit' = quit")
    print("-------------------\n")

    # check ollama is running
    try:
        ollama.list()
    except Exception:
        print("Ollama is not running!")
        print("Start it by running: ollama serve")
        sys.exit(1)

    print("Loading model...")
    try:
        ollama.chat(model=MODEL, messages=[{"role": "user", "content": "hi"}])
        print("Ready.\n")
    except Exception as e:
        print(f"Could not load model: {e}")
        print(f"Try: ollama pull {MODEL}")
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Bye!")
                break

            if user_input.lower() == "clear":
                clear_memory()
                continue

            start = time.time()
            ask(user_input)
            elapsed = time.time() - start
            print(f"({elapsed:.1f}s)\n")

        except KeyboardInterrupt:
            print("\nType 'exit' to quit.\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
