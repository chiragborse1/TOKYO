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
import sys
from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        # First, check if browser is already running
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            contexts = browser.contexts
            if contexts:
                page = contexts[0].new_page()
                page.goto('{url}')
                print('Opened new tab in existing browser.')
            browser.close()
            sys.exit(0)
        except Exception:
            # If it fails, the browser isn't running. We must launch it.
            pass

        # Launch a persistent context to save cookies, logins, and avoid incognito mode
        profile_dir = "C:\\\\Users\\\\chira\\\\Downloads\\\\TOKYO\\\\data\\\\browser_profile"
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            args=['--remote-debugging-port=9222']
        )
        
        # In a persistent context, pages[0] is usually the default blank tab
        if len(browser_context.pages) > 0:
            page = browser_context.pages[0]
        else:
            page = browser_context.new_page()
            
        page.goto('{url}')
        
        # Keep the browser open until the user closes the last page
        page.wait_for_event("close", timeout=0)
        browser_context.close()
except Exception as e:
    print("Browser error:", str(e))
"""
        import os
        import tempfile
        script_path = os.path.join(tempfile.gettempdir(), "tokyo_browser_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)
        
        # Run detached from the server so the GUI can actually render on the user's desktop
        CREATE_NEW_CONSOLE = 0x00000010
        import os
        env = os.environ.copy()
        env["NODE_OPTIONS"] = "--no-warnings"
        
        subprocess.Popen(
            ["python", script_path], 
            creationflags=CREATE_NEW_CONSOLE,
            close_fds=True,
            env=env
        )
        return "Browser process launched/tab opened for: " + url
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

def _run_browser_action(action, selector=None, text=None):
    """Helper to connect to the running browser and execute an action safely via arguments."""
    script = f"""
import sys
from playwright.sync_api import sync_playwright

action = sys.argv[1]
selector = sys.argv[2] if len(sys.argv) > 2 else None
text = sys.argv[3] if len(sys.argv) > 3 else None

try:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        if action == "click" and selector:
            page.click(selector)
            print(f"Clicked: {{selector}}")
        elif action == "type" and selector and text is not None:
            page.fill(selector, text)
            print(f"Typed into {{selector}}")
        elif action == "get_text":
            print(page.inner_text("body")[:2000])
        elif action == "close":
            page.close()
            print("Browser closed")
            
        browser.close()
except Exception as e:
    print(str(e))
"""
    try:
        import os
        import tempfile
        script_path = os.path.join(tempfile.gettempdir(), "tokyo_action_script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)
            
        args = ["python", script_path, action]
        if selector is not None:
            args.append(selector)
        if text is not None:
            args.append(text)
            
        import os
        import tempfile
        env = os.environ.copy()
        env["NODE_OPTIONS"] = "--no-warnings"
        env["PYTHONIOENCODING"] = "utf-8"
        
        CREATE_NO_WINDOW = 0x08000000
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
            env=env,
            creationflags=CREATE_NO_WINDOW
        )
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        return result.stdout.strip() or "Success"
    except Exception as e:
        return f"Error executing browser action: {str(e)}"

def browser_click(selector):
    return _run_browser_action("click", selector)

def browser_type(selector, text):
    return _run_browser_action("type", selector, text)

def browser_get_text():
    return _run_browser_action("get_text")

def browser_close():
    return _run_browser_action("close")

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

You can output multiple <tool> blocks at once to perform actions sequentially.

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
- browser_open(url): opens a visible Chrome browser with persistent session.
- browser_click(selector): clicks an element. ALWAYSS prefer basic locators if possible, e.g. text="Like" or [aria-label="Search"] or #submit_btn. DO NOT use complex unverified XPath.
- browser_type(selector, text): types text into an element. Always prefer basic locators, e.g. [name="search_query"] or text="Search".
- browser_get_text()
- browser_screenshot(filename)
- browser_close()

Confirm before deleting files.
"""