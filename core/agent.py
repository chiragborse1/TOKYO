from groq import Groq
from dotenv import load_dotenv
from core.tools import TOOLS, get_tools_description
from core.memory import save_message, load_history, clear_memory
import os
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are TOKYO, a powerful personal AI assistant.
You are efficient, smart, and always helpful.
You help your owner with files, coding, research, emails and anything they need.
You always confirm before deleting or modifying important files.

The user's Windows PC details:
- Username: chira
- Home path: C:\\Users\\chira\\
- Downloads folder: C:\\Users\\chira\\Downloads
- Desktop: C:\\Users\\chira\\Desktop
- Documents: C:\\Users\\chira\\Documents

""" + get_tools_description()


import inspect

def execute_tool(tool_name, args_str):
    if tool_name not in TOOLS:
        return "Unknown tool: " + tool_name

    tool = TOOLS[tool_name]

    if not args_str.strip() or args_str.strip().lower() == "none":
        return tool()

    try:
        sig = inspect.signature(tool)
        num_params = len(sig.parameters)
        if num_params == 1:
            args = [args_str.strip()]
        else:
            args = [arg.strip() for arg in args_str.split("|") if arg.strip()]
    except Exception:
        args = [arg.strip() for arg in args_str.split("|") if arg.strip()]

    try:
        return tool(*args)
    except TypeError:
        try:
            return tool()
        except Exception as e:
            return "Error: " + str(e)



def chat(user_message):
    try:
        # Load history first
        history = load_history(6)

        # Save user message
        save_message("user", user_message)

        # Build messages including current user message
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": user_message}
        ]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )

        assistant_message = response.choices[0].message.content

        if not assistant_message:
            return "TOKYO got no response. Try again."

        # Check if TOKYO wants to use a tool
        tool_match = re.search(r'<tool>.*?TOOL:\s*(\w+).*?ARGS:\s*(.*?)\s*</tool>', assistant_message, re.DOTALL)
        if not tool_match:
            # Fallback for old format
            tool_match = re.search(r'TOOL:\s*(\w+)[^\w].*?ARGS:\s*(.*?)(?=\n\n|\Z)', assistant_message, re.DOTALL)

        if tool_match:
            tool_name = tool_match.group(1).strip()
            args_str = tool_match.group(2).strip()

            tool_result = execute_tool(tool_name, args_str)

            save_message("assistant", assistant_message)
            save_message("user", "Tool result: " + str(tool_result))

            # Build updated messages for final response
            updated_history = load_history(8)
            final_messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                *updated_history
            ]

            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=final_messages,
                temperature=0.7,
                max_tokens=512
            )

            assistant_message = final_response.choices[0].message.content
            assistant_message = re.sub(r'<tool>.*?</tool>', '', assistant_message, flags=re.DOTALL | re.IGNORECASE)
            assistant_message = re.sub(r'TOOL:\s*\w+.*?ARGS:\s*.*', '', assistant_message, flags=re.DOTALL).strip()

        # Save final response
        save_message("assistant", assistant_message)

        return assistant_message

    except Exception as e:
        print("Chat error: " + str(e))
        return "Error: " + str(e)


def clear_history():
    return clear_memory()