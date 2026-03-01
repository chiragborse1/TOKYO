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
            if "|" in args_str:
                args = [arg.strip() for arg in args_str.split("|") if arg.strip()]
            else:
                # Fallback if LLM uses comma instead of pipe
                args = [arg.strip() for arg in args_str.split(",", num_params - 1) if arg.strip()]
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
        # Load history once at the start
        history = load_history(6)

        # Save the initial user message
        save_message("user", user_message)

        # Initialize the local message history array
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history,
            {"role": "user", "content": user_message}
        ]

        iteration = 0
        max_iterations = 5

        while iteration < max_iterations:
            iteration += 1

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=512
            )

            assistant_message = response.choices[0].message.content

            if not assistant_message:
                return "TOKYO got no response. Try again."

            # Find ALL tool usages in the response, gracefully handling absent TOOL: prefix
            tool_matches = list(re.finditer(r'<tool>\s*(?:TOOL:\s*)?([a-zA-Z0-9_]+)\s*.*?ARGS:\s*(.*?)\s*</tool>', assistant_message, re.DOTALL | re.IGNORECASE))
            
            if not tool_matches:
                # Fallback for old format
                tool_matches = list(re.finditer(r'TOOL:\s*([a-zA-Z0-9_]+)[^\w].*?ARGS:\s*(.*?)(?=\n\n|\Z)', assistant_message, re.DOTALL | re.IGNORECASE))

            # If no tools were found, we are done!
            if not tool_matches:
                clean_message = re.sub(r'<tool>.*?</tool>', '', assistant_message, flags=re.DOTALL | re.IGNORECASE).strip()
                clean_message = re.sub(r'TOOL:\s*\w+.*?ARGS:\s*.*', '', clean_message, flags=re.DOTALL | re.IGNORECASE).strip()
                
                # Save the final conversational response
                save_message("assistant", assistant_message)
                return clean_message

            # Tools were found! Save the assistant's thought process
            save_message("assistant", assistant_message)
            messages.append({"role": "assistant", "content": assistant_message})
            
            # Execute every tool requested
            combined_results = []
            for match in tool_matches:
                tool_name = match.group(1).strip().lower()
                args_str = match.group(2).strip()
                
                tool_result = execute_tool(tool_name, args_str)
                combined_results.append(f"Tool `{tool_name}` result: {tool_result}")

            # Feed the results back to the LLM in the next iteration locally
            results_str = "Tool results:\n" + "\n".join(combined_results)
            save_message("user", results_str)
            messages.append({"role": "user", "content": results_str})

        return "Error: Maximum tool execution iterations reached."

    except Exception as e:
        print("Chat error: " + str(e))
        return "Error: " + str(e)


def clear_history():
    return clear_memory()