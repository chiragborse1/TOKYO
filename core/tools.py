import os
import subprocess
import requests
from bs4 import BeautifulSoup
import datetime

def create_file(filepath, content=""):
    """Create a new file with optional content"""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f" File created: {filepath}"
    except Exception as e:
        return f" Error creating file: {str(e)}"

def read_file(filepath):
    """Read contents of a file"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f" Error reading file: {str(e)}"

def delete_file(filepath):
    """Delete a file"""
    try:
        os.remove(filepath)
        return f" File deleted: {filepath}"
    except Exception as e:
        return f" Error deleting file: {str(e)}"

def list_files(directory="."):
    """List all files in a directory"""
    try:
        files = os.listdir(directory)
        return f" Files in {directory}:\n" + "\n".join(files)
    except Exception as e:
        return f" Error listing files: {str(e)}"

def create_folder(folderpath):
    """Create a new folder"""
    try:
        os.makedirs(folderpath, exist_ok=True)
        return f" Folder created: {folderpath}"
    except Exception as e:
        return f" Error creating folder: {str(e)}"

def move_file(source, destination):
    """Move a file from source to destination"""
    try:
        import shutil
        shutil.move(source, destination)
        return f" Moved {source} to {destination}"
    except Exception as e:
        return f" Error moving file: {str(e)}"

def search_web(query):
    """Search the web using DuckDuckGo"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for result in soup.find_all("a", class_="result__a", limit=5):
            results.append(f"• {result.get_text()} → {result['href']}")
        if results:
            return "Search Results:\n" + "\n".join(results)
        return "No results found."
    except Exception as e:
        return f" Error searching web: {str(e)}"

def fetch_webpage(url):
    """Fetch and read content from a webpage"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:2000] + "..." if len(text) > 2000 else text
    except Exception as e:
        return f" Error fetching webpage: {str(e)}"



def run_python_code(code):
    """Run Python code and return output"""
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return f" Output:\n{result.stdout}"
        else:
            return f" Error:\n{result.stderr}"
    except Exception as e:
        return f" Error running code: {str(e)}"

def open_application(app_name):
    """Open an application on Windows"""
    try:
        os.startfile(app_name)
        return f" Opened: {app_name}"
    except Exception as e:
        return f" Error opening app: {str(e)}"

def get_system_info():
    """Get basic system information"""
    try:
        info = {
            "datetime": str(datetime.datetime.now()),
            "current_directory": os.getcwd(),
            "platform": os.name
        }
        return "\n".join([f"{k}: {v}" for k, v in info.items()])
    except Exception as e:
        return f" Error getting system info: {str(e)}"


TOOLS = {
    "create_file": create_file,
    "read_file": read_file,
    "delete_file": delete_file,
    "list_files": list_files,
    "create_folder": create_folder,
    "move_file": move_file,
    "search_web": search_web,
    "fetch_webpage": fetch_webpage,
    "run_python_code": run_python_code,
    "open_application": open_application,
    "get_system_info": get_system_info,
}

def get_tools_description():
    """Returns a description of all tools for the AI"""
    return """
You have access to these tools. To use a tool respond with EXACTLY this format:
TOOL: tool_name
ARGS: argument1 | argument2

Available tools:
- create_file(filepath, content) → Create a file
- read_file(filepath) → Read a file
- delete_file(filepath) → Delete a file
- list_files(directory) → List files in a folder
- create_folder(folderpath) → Create a folder
- move_file(source, destination) → Move a file
- search_web(query) → Search the internet
- fetch_webpage(url) → Read a webpage
- run_python_code(code) → Execute Python code
- open_application(app_name) → Open an app
- get_system_info() → Get system info

Always confirm with the user before deleting files.
"""