from playwright.sync_api import sync_playwright
import os
import subprocess
import requests
from bs4 import BeautifulSoup
import datetime
from dotenv import load_dotenv

load_dotenv()

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
    """Search the web using Serper API"""
    try:
        api_key = os.getenv("SERPER_API_KEY")
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        payload = {"q": query, "num": 5}
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=payload,
            timeout=10
        )
        data = response.json()
        results = []

        # Answer box if available
        if data.get("answerBox"):
            answer = data["answerBox"].get("answer") or data["answerBox"].get("snippet")
            if answer:
                results.append(f"📌 Quick Answer: {answer}")

        # Organic results
        for item in data.get("organic", [])[:5]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            results.append(f"• {title}\n  {snippet}\n  🔗 {link}")

        if results:
            return "🌐 Search Results:\n\n" + "\n\n".join(results)

        return "No results found for: " + query

    except Exception as e:
        return f"❌ Error searching web: {str(e)}"

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

# -------------------------------------------------
# BROWSER TOOLS
# -------------------------------------------------

def browser_open(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        script = f"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('{url}')
    input('Browser open. Press Enter to close...')
    browser.close()
"""
        script_path = "C:\\Users\\chira\\Downloads\\TOKYO\\data\\browser_script.py"
        with open(script_path, "w") as f:
            f.write(script)
        subprocess.Popen(["python", script_path])
        return "Browser opened at: " + url
    except Exception as e:
        return "Error: " + str(e)

def browser_screenshot(filename="screenshot.png"):
    try:
        path = "C:\\Users\\chira\\Downloads\\" + filename
        script = f"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.screenshot(path=r'{path}')
    browser.close()
"""
        script_path = "C:\\Users\\chira\\Downloads\\TOKYO\\data\\screenshot_script.py"
        with open(script_path, "w") as f:
            f.write(script)
        result = subprocess.run(["python", script_path], capture_output=True, timeout=15)
        return "Screenshot saved: " + path
    except Exception as e:
        return "Error: " + str(e)

def browser_click(selector):
    return "Use browser_open first, then interact manually for now."

def browser_type(selector, text):
    return "Use browser_open first, then interact manually for now."

def browser_get_text():
    return "Use browser_open first, then interact manually for now."

def browser_close():
    return "Close the browser window manually."

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
    "browser_open": browser_open,
    "browser_click": browser_click,
    "browser_type": browser_type,
    "browser_get_text": browser_get_text,
    "browser_screenshot": browser_screenshot,
    "browser_close": browser_close,
}

def get_tools_description():
    return """
You have access to these tools. Use EXACTLY this format:
<tool>
TOOL: tool_name
ARGS: argument1 | argument2
</tool>

Tools:
- create_file(filepath, content)
- read_file(filepath)
- delete_file(filepath)
- list_files(directory)
- create_folder(folderpath)
- move_file(source, destination)
- search_web(query)
- fetch_webpage(url)
- run_python_code(code)
- open_application(app_name)
- get_system_info()
- browser_open(url)
- browser_click(selector)
- browser_type(selector, text)
- browser_get_text()
- browser_screenshot(filename)
- browser_close()

Confirm before deleting files.
"""