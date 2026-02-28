from groq import Groq
from dotenv import load_dotenv
from core.tools import TOOLS, get_tools_description
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

conversation_history = []

def execute_tool(tool_name, args_str):
    """Execute a tool by name with arguments"""
    if tool_name not in TOOLS:
        return f"❌ Unknown tool: {tool_name}"
    
    tool = TOOLS[tool_name]
    
    # If no args needed
    if not args_str.strip() or args_str.strip().lower() == "none":
        return tool()
    
    # Parse arguments
    args = [arg.strip() for arg in args_str.split("|") if arg.strip()]
    
    # Try with args first, then without
    try:
        return tool(*args)
    except TypeError:
        try:
            return tool()
        except Exception as e:
            return f"❌ Error: {str(e)}"


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
        max_tokens=1024
    )
    
    assistant_message = response.choices[0].message.content

    # Check if TOKYO wants to use a tool
    tool_match = re.search(r'TOOL:\s*(\w+)[^\w].*?ARGS:\s*(.+)', assistant_message, re.DOTALL)
    
    if tool_match:
        tool_name = tool_match.group(1).strip()
        args_str = tool_match.group(2).strip()
        
        # Execute the tool
        tool_result = execute_tool(tool_name, args_str)
        
        # Send tool result back to TOKYO
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        conversation_history.append({
            "role": "user",
            "content": f"Tool result: {tool_result}"
        })
        
        # Get final response
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *conversation_history
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        assistant_message = final_response.choices[0].message.content
        
        # Clean any raw TOOL: text from final response
        assistant_message = re.sub(r'TOOL:\s*\w+.*?ARGS:\s*.+', '', assistant_message, flags=re.DOTALL).strip()
    
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message


def clear_history():
    global conversation_history
    conversation_history = []
    return "Conversation history cleared."