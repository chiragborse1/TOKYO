from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are TOKYO, a powerful personal AI assistant.
You are efficient, smart , and always helpful.
You help your owner with files, coding, research, emails and anything they need.
You always confirm before deleting or modifying important files.
You remember context within a conversation.
Keep responses clear and concise.
"""

conversation_history = []

def chat(user_message):
    """Send a message to TOKYO and get a response"""

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history
        ],
        temperature=0.7,
        max_tokens = 1024
    )

    assistant_message =response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message

def clear_history():
    """Clear converasation history"""
    global conversation_history
    conversation_history = []
    return "Conversation history cleared."
    