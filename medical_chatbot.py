#!/usr/bin/env python3
"""Medical Chatbot using the OpenAI API.

This tool answers general medical questions, but it is not a substitute
for professional medical advice. Always consult a qualified healthcare
professional for medical concerns.
"""
import os
import sys

import openai


SYSTEM_PROMPT = (
    "You are a knowledgeable medical professional who provides "
    "concise answers. Always remind the user to consult a real "
    "healthcare professional for any medical concerns."
)


def ask_bot(question: str) -> str:
    """Send a question to the OpenAI ChatCompletion API and return the reply."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    openai.api_key = api_key
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message["content"].strip()


def main() -> None:
    print("Welcome to the Medical Chatbot.")
    print(
        "This tool can provide general medical information, "
        "but it does not replace professional medical advice."
    )
    print("Type 'exit' or 'quit' to stop.")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break
        try:
            reply = ask_bot(user_input)
        except Exception as exc:  # catch network or API errors
            print(f"Error: {exc}")
            continue
        print("Bot:", reply)
        print("Remember to always seek medical advice from a qualified professional.")


if __name__ == "__main__":
    main()
