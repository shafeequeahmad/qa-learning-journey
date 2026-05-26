import os
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import TypedDict, Dict, List, Optional
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END

env_path = Path(r"D:\Shafeeque\AI skilled QA\qa-learning-journey\qa-learning\.env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise SystemExit("Error: Please set your GROQ_API_KEY in the .env file.")

llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", groq_api_key=api_key)
SESSION_FILE = "session_state.json"
STORAGE_STATE = "storage_state.json"

# 1. Define State
class QAState(TypedDict):
    user_instruction: str
    url: str
    website_name: str
    app_config: Dict[str, str]
    dom_content: str
    page_title: str
    csv_filename: str
    tcs_csv: str
    user_feedback: str
    intent: str
    qa_answer: str
    approved: bool
    mode: str # 'menu', 'draft', 'code', 'crawl'
    selected_csvs: List[str]
    pom_json_str: str
    execution_output: str
    retries: int
    crawl_queue: List[str]
    visited_urls: List[str]

# Utilities
def save_session(state: QAState):
    with open(SESSION_FILE, "w") as f:
        json.dump({k: state.get(k) for k in ["website_name", "url"]}, f)

def tag_automated_csv(website: str, filename: str):
    path = Path("TCs") / website / filename
    if path.exists():
        content = path.read_text(encoding="utf-8")
        if "# STATUS: AUTOMATED" not in content:
            tag = f"# STATUS: AUTOMATED - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            path.write_text(tag + content, encoding="utf-8")
            print(f"[Agent] Tagged {filename} as AUTOMATED.")

# 2. Define Nodes
def init_session(state: QAState) -> dict:
    print("\n" + "="*50 + "\n  AI QA AGENT v7.0 (Menu-Driven)\n" + "="*50)
    
    # Resume Logic
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            old = json.load(f)
        if input(f"Resume project '{old.get('website_name')}'? (y/n): ").lower() == 'y':
            return {"url": old.get("url"), "website_name": old.get("website_name"), "mode": "menu"}

    url = input("[Enter Website URL]: ").strip()
    if not url.startswith("http"): url = "https://" + url
    return {"url": url, "mode": "menu", "retries": 0, "intent": ""}

def analyze_request(state: QAState) -> dict:
    if state.get("website_name"): return {}
    print("[Agent] Analyzing website structure...")
    res = (PromptTemplate.from_template("Extract WEBSITE NAME from URL: {u}\nOut:").pipe(llm)).invoke({"u": state["url"]}).content.strip()
    w = res.split("\n")[0].replace(" ", "_").replace("WEBSITE:", "").strip() or "App"
    save_session({"url": state["url"], "website_name": w})
    return {"website_name": w}

def main_menu(state: QAState) -> dict:
    print(f"\n--- PROJECT: {state['website_name']} ---")
    print("1. Code Now (Automate TCs)")
    print("2. Write TCs (Drafting)")
    print("3. Auto-Crawl (Smart)")
    print("4. Exit")
    
    while True:
        choice = input("Choice: ").strip().lower()
        if choice == '1': return {"mode": "code", "intent": "automate"}
        if choice == '2': return {"mode": "draft", "intent": "draft"}
        if choice == '3': return {"mode": "crawl", "intent": "crawl"}
        if choice in ['4', 'exit', 'quit']: exit(0)
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def auto_crawl(state: QAState) -> dict:
    print(f"\n[Mode: Auto-Crawl]")
    start_url = input(f"Enter starting URL to crawl (or press Enter for '{state['url']}'): ").strip()
    if not start_url:
        start_url = state["url"]
    if not start_url.startswith("http"): start_url = "https://" + start_url
    return {"url": start_url, "crawl_queue": [start_url], "visited_urls": [], "mode": "crawl"}

def next_crawl_step(state: QAState) -> dict:
    queue = state.get("crawl_queue", [])
    visited = state.get("visited_urls", [])
    
    current_url = state.get("url")
    if current_url and current_url not in visited:
        visited.append(current_url)
        
    dom = state.get("dom_content", "")
    links = re.findall(r"href='([^']+)'", dom)
    
    base_domain = current_url.split("/")[2] if current_url and "://" in current_url else ""
    
    new_urls = []
    for link in links:
        if link.startswith("/"):
            link = current_url.split("://")[0] + "://" + base_domain + link
            
        if base_domain in link and link not in visited and link not in queue:
            new_urls.append(link)
            
    # Add top 5 new links to avoid massive queues
    for link in new_urls[:5]:
        if link not in queue:
            queue.append(link)
            
    if queue:
        next_url = queue.pop(0)
        print(f"\n[Auto-Crawl] Next target: {next_url}")
        print(f"[Auto-Crawl] Queue size: {len(queue)}")
        return {"url": next_url, "crawl_queue": queue, "visited_urls": visited, "intent": "crawl"}
    return {}

def draft_setup(state: QAState) -> dict:
    print(f"\n[Mode: Drafting]")
    new_url = input(f"Which page next? (Enter URL or press Enter for '{state['url']}'): ").strip()
    if new_url:
        if not new_url.startswith("http"): new_url = "https://" + new_url
        return {"url": new_url, "intent": "draft"}
    return {"intent": "draft"}

def scrape_url(state: QAState) -> dict:
    target_url = state["url"]
    print(f"[Agent] Navigating to Target Page: {target_url}")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=STORAGE_STATE if os.path.exists(STORAGE_STATE) else None)
            page = context.new_page()
            page.goto(target_url, timeout=30000)
            page.wait_for_timeout(3000) # Crucial: Wait for JS-based redirects to login
            
            # Proactive Login Detection (Only if redirected away from target to a login page)
            current_url = page.url.lower()
            is_login_page = "login" in current_url or page.locator("input[type='password']").is_visible()
            
            # If we asked for dashboard but landed on login
            if is_login_page and "login" not in target_url.lower():
                print(f"\n[ALERT] Redirected to login while trying to access: {target_url}")
                if input("Perform login now to proceed inside? (y/n): ").lower() == 'y':
                    user = input("Username: ").strip()
                    pw = input("Password: ").strip()
                    
                    # Fill credentials on WHATEVER page we are currently on (the login page)
                    page.locator("input[name='username'], input[placeholder*='Username']").first.fill(user)
                    page.locator("input[type='password']").fill(pw)
                    
                    # Try clicking the Login button explicitly
                    login_btn = page.locator("button[type='submit'], .orangehrm-login-button")
                    if login_btn.is_visible():
                        login_btn.click()
                    else:
                        page.keyboard.press("Enter")
                        
                    page.wait_for_load_state("networkidle")
                    page.wait_for_timeout(3000) # Wait for redirect to start
                    
                    if "login" in page.url.lower():
                        print("[Error] Login failed. Incorrect credentials or blocked. Still on Login page.")
                    else:
                        # Save session for future pages
                        context.storage_state(path=STORAGE_STATE)
                        print(f"[Agent] Login successful. Verifying navigation to: {target_url}")
                    
                    # Force navigation and WAIT for URL to match
                    page.goto(target_url, timeout=30000)
                    
                    # Wait for both 'load' and 'networkidle' for maximum stability
                    page.wait_for_load_state("load")
                    page.wait_for_load_state("networkidle")
                    
                    # Wait up to 10 seconds for the URL to settle (Handles SPA redirects)
                    for _ in range(10):
                        if target_slug in page.url.lower(): break
                        page.wait_for_timeout(1000)
                    
                    # Final stabilization wait to ensure Vue/React components are rendered
                    page.wait_for_timeout(3000) 
            
            # FINAL CHECK: Ensure we are not drafting the wrong page
            current_url = page.url.lower()
            print(f"[Agent] FINAL Browser URL for Drafting: {current_url}")
            
            # Looser check: see if the slug or target is contained in the current URL
            target_slug = target_url.rstrip("/").split("/")[-1]
            if "login" in current_url and target_slug not in current_url:
                print(f"[Error] Failed to reach {target_url}. Browser stayed on Login page.")
                browser.close()
                return {"dom_content": "Error: Navigation failed to reach target page.", "page_title": "error", "intent": "fail"}

            # Better Page Title generation
            title = page.title()
            url_slug = target_url.rstrip("/").split("/")[-1] or "index"
            clean_title = title.replace(" ", "_").lower()
            if "orangehrm" in clean_title and len(clean_title) < 15:
                clean_title = f"{clean_title}_{url_slug}"
            
            # Build a Semantic DOM (Comprehensive coverage for all QA-relevant elements)
            soup = BeautifulSoup(page.content(), 'html.parser')
            semantic_elements = []
            
            # Target standard interactive elements + OrangeHRM custom components
            for tag in soup.find_all(['button', 'input', 'select', 'label', 'a', 'h1', 'h2', 'h3', 'th', 'tr', 'td', 'span', 'i', 'div']):
                classes = " ".join(tag.get('class', []))
                role = tag.get('role', '')
                aria = tag.get('aria-label', '')
                
                # Filter for meaningful elements only to keep context window clean
                is_qa_relevant = any(x in classes for x in ["oxd-", "orangehrm-"]) or role or aria or tag.name in ['button', 'input', 'select', 'a', 'th', 'h1', 'h2', 'h3']
                
                if not is_qa_relevant and tag.name in ['div', 'span', 'i', 'td', 'tr']:
                    continue
                
                text = tag.get_text(strip=True)
                t_type = tag.get('type', 'text')
                placeholder = tag.get('placeholder', '')
                
                # Extract options for standard selects
                options = ""
                if tag.name == 'select':
                    options = " Options: " + ", ".join([opt.get_text(strip=True) for opt in tag.find_all('option')])

                href_str = ""
                if tag.name == 'a':
                    href = tag.get('href')
                    if href:
                        href_str = f" href='{href}'"

                if text or placeholder or role or aria or href_str:
                    attr_str = f"type='{t_type}' role='{role}' aria='{aria}' placeholder='{placeholder}'{options}{href_str}"
                    semantic_elements.append(f"<{tag.name} {attr_str}>{text}</{tag.name}>")
            
            dom = "\n".join(semantic_elements)[:30000] # High limit for total coverage
            browser.close()
            return {"dom_content": dom, "page_title": clean_title, "url": target_url, "intent": "success"}
    except Exception as e: return {"dom_content": f"Error: {e}", "page_title": "error", "intent": "fail"}

def draft_tcs(state: QAState) -> dict:
    if state.get("intent") == "fail": return {} # Safeguard
    print(f"[Agent] Drafting Test Cases for {state.get('page_title', 'Page')}...")
    
    feedback_context = ""
    if state.get("user_feedback"):
        feedback_context = f"\n[USER FEEDBACK TO INCORPORATE]: {state['user_feedback']}\n"
    
    prompt = PromptTemplate.from_template(
        "Expert QA Engineer. You are on the following page: {title}\n"
        "TASK: Provide TOTAL TEST COVERAGE (Smoke, Sanity, Regression) for the CURRENT PAGE ONLY.\n"
        "COVERAGE CATEGORIES:\n"
        "1. NAVIGATION: Side menus, breadcrumbs, and hyperlinks.\n"
        "2. DATA ENTRY: Text boxes, date pickers, and dropdowns (check specific options).\n"
        "3. DATA DISPLAY: Tables, headers, grid data, and records-found text.\n"
        "4. ACTIONS: Buttons (Save, Reset, Add), Icons (Edit, Delete), and Search.\n"
        "5. VALIDATION: Mandatory fields, format checks, and error/success messages.\n"
        "\n{feedback}\n"
        "Output CSV ONLY.\n"
        "First line: FILENAME: {title}_tc.csv\n"
        "Columns: TC_Name,Priority,Label,Description,Locator,Visual_Checks_Required,Expected_Result\n"
        "Constraints:\n"
        "- The 'Locator' column MUST contain the exact, highly stable CSS or Playwright selector (e.g. input[name='username'], button[type='submit'], .oxd-button, etc.) found in the DOM for the element being interacted with. Never make up a locator. If it is a generic page validation, put 'N/A'.\n"
        "Labels: Smoke, Sanity, Regression\nDOM: {d}\nCSV:"
    )
    res = (prompt | llm).invoke({
        "d": state["dom_content"], 
        "title": state.get("page_title", "page"),
        "feedback": feedback_context
    })
    raw = res.content.strip(); lines = raw.split('\n'); f = f"{state.get('page_title', 'page')}_tc.csv"; csv_l = []
    for l in lines:
        if l.startswith("FILENAME:"): f = l.replace("FILENAME:", "").strip()
        else: csv_l.append(l)
    csv_t = "\n".join(csv_l).replace('```csv', '').replace('```', '').strip()
    d = Path("TCs") / state.get("website_name", "App"); d.mkdir(parents=True, exist_ok=True); (d / f).write_text(csv_t, encoding="utf-8")
    return {"tcs_csv": csv_t, "csv_filename": f}

def human_approval(state: QAState) -> dict:
    if state.get("intent") == "fail": return {"mode": "menu", "approved": False}
    print(f"\n--- DRAFTED TCs ---\n{state['tcs_csv']}\n---")
    fed = input("Approve? (y/n), type 'exit', or type feedback: ").strip()
    if fed.lower() in ['exit', 'quit']: exit(0)
    if fed.lower() == 'y': return {"approved": True, "mode": "menu"}
    return {"approved": False, "user_feedback": fed}

def automation_setup(state: QAState) -> dict:
    print(f"\n[Mode: Automation]")
    d = Path("TCs") / state["website_name"]
    if not d.exists(): 
        print("[Agent] TCs folder not found.")
        return {"mode": "menu", "intent": "no_tcs"}
    
    files = [f.name for f in d.glob("*.csv")]
    if not files:
        print("[Agent] No CSV files found in TCs folder.")
        return {"mode": "menu", "intent": "no_tcs"}
        
    print(f"Available TCs: {files}")
    choice = input("Enter TC Filename or 'ALL': ").strip()
    
    selected = []
    if choice.lower() == 'all':
        for f in d.glob("*.csv"):
            content = f.read_text(encoding="utf-8")
            if "# STATUS: AUTOMATED" in content:
                print(f"  -> Skipping {f.name} (Already Automated)")
            else:
                selected.append(f.name)
    else:
        selected = [choice] if choice in files else []
        
    if not selected:
        print("[Agent] No new TCs selected.")
        return {"mode": "menu", "intent": "no_tcs"}
    
    return {"selected_csvs": selected, "mode": "code"}

def collect_config(state: QAState) -> dict:
    if state.get("app_config"): return {}
    print("\n[Settings]")
    user = input("Test Username: ").strip()
    pw = input("Test Password: ").strip()
    return {"app_config": {"base_url": state["url"], "username": user, "password": pw}}

def generate_pom(state: QAState) -> dict:
    print("\n[Agent] Generating Code for selected TCs...")
    d = Path("TCs") / state["website_name"]
    
    # Clean Sweep Reminder
    print("\n" + "!"*40 + "\n  REMINDER: Clean 'pages/' and 'tests/'\n" + "!"*40 + "\n")
    
    tcs = ""
    for fname in state["selected_csvs"]:
        f = d / fname
    for f in state["selected_csvs"]:
        tcs += f"\n--- {f} ---\n" + (Path("TCs") / state["website_name"] / f).read_text(encoding="utf-8")
    
    error_feedback = ""
    if state.get("execution_output"):
        error_feedback = f"\n[PREVIOUS FAILURE LOG]:\n{state['execution_output'][-2000:]}\n[FIX THE ABOVE ERRORS]"
    
    prompt = PromptTemplate.from_template(
        "Expert Playwright POM Architect. Scaffold framework.\n"
        "STRICT FORMAT RULE: You MUST output files in this EXACT format:\n"
        "--- FILE: constants/app_constants.py ---\n"
        "<code>\n"
        "--- FILE: pages/example_page.py ---\n"
        "<code>\n"
        "--- FILE: tests/test_example.py ---\n"
        "<code>\n"
        "\nCONSTRAINTS:\n"
        "1. Create `constants/app_constants.py` with BASE_URL and standard credentials.\n"
        "2. POM in `pages/`.\n"
        "3. Descriptive test name in `tests/`.\n"
        "4. Dictionary locators. You MUST use the exact locators specified in the 'Locator' column of the CSV below. DO NOT guess or assume older IDs like '#txtUsername' if the CSV specifies a different locator.\n"
        "5. conftest.py with session browser fixture.\n"
        "6. MUST IMPORT PARENTS (e.g. from pages.base_page import BasePage).\n"
        "7. Pytest markers (Smoke/Sanity/Regression).\n"
        "8. [CRITICAL] Use constants.BASE_URL for all navigation and URL assertions.\n"
        "9. [CRITICAL] DO NOT use open() or csv.reader(). Hardcode the data from TCS below.\n"
        "10. [CRITICAL] NO CONVERSATIONAL TEXT. Only output the code blocks.\n"
        "{ef}\nTCS:\n{tcs}\n\nTARGET URL: {url}\n\nCSV DATA TO AUTOMATE:"
    )
    res = (prompt | llm).invoke({"tcs": tcs, "ef": error_feedback, "url": state.get("url", "")})
    return {"pom_json_str": res.content.strip()}

def save_pom_files(state: QAState) -> dict:
    raw = state.get("pom_json_str", "")
    if "--- FILE:" not in raw:
        print("[Error] AI generated code in wrong format. Retrying...")
        return {"intent": "fail"}
    
    print("[Agent] Scaffolding files...")
    files = re.split(r'--- FILE: (.*?) ---', raw)
    for i in range(1, len(files), 2):
        path = Path(files[i].strip())
        path.parent.mkdir(parents=True, exist_ok=True)
        content = files[i+1].strip().replace('```python', '').replace('```', '')
        path.write_text(content, encoding="utf-8")
        print(f"  -> Created {path}")
    return {"intent": "success"}

def execute_tests(state: QAState) -> dict:
    if not os.path.exists("tests"):
        print("[Error] 'tests/' folder was not created.")
        return {"retries": state.get("retries", 0) + 1, "execution_output": "Tests folder missing"}
        
    print("[Agent] Running Pytest...")
    res = subprocess.run(["pytest", "tests/", "-v"], capture_output=True, text=True)
    if res.returncode == 0:
        for f in state["selected_csvs"]: tag_automated_csv(state["website_name"], f)
        print("[Success] All tests passed!")
        return {"mode": "menu", "retries": 0}
    
    return {"retries": state.get("retries", 0) + 1, "execution_output": res.stdout + res.stderr}

# 3. Graph
workflow = StateGraph(QAState)
workflow.add_node("init", init_session)
workflow.add_node("analyze", analyze_request)
workflow.add_node("menu", main_menu)
workflow.add_node("crawl", auto_crawl)
workflow.add_node("next_crawl", next_crawl_step)
workflow.add_node("draft_setup", draft_setup)
workflow.add_node("scrape", scrape_url)
workflow.add_node("draft", draft_tcs)
workflow.add_node("approval", human_approval)
workflow.add_node("auto_setup", automation_setup)
workflow.add_node("config", collect_config)
workflow.add_node("generate", generate_pom)
workflow.add_node("save", save_pom_files)
workflow.add_node("execute", execute_tests)

workflow.set_entry_point("init")
workflow.add_edge("init", "analyze")
workflow.add_edge("analyze", "menu")

workflow.add_conditional_edges("menu", lambda x: x["mode"], {"draft": "draft_setup", "code": "auto_setup", "crawl": "crawl", "menu": "menu"})
workflow.add_edge("crawl", "scrape")
workflow.add_edge("next_crawl", "scrape")

workflow.add_edge("draft_setup", "scrape")
workflow.add_conditional_edges("scrape", lambda x: x["intent"], {"success": "draft", "fail": "menu"})
workflow.add_edge("draft", "approval")

workflow.add_conditional_edges("approval", 
    lambda x: "next" if x.get("approved") and x.get("crawl_queue") else ("menu" if x.get("approved") else "draft"),
    {"next": "next_crawl", "menu": "menu", "draft": "draft"}
)

workflow.add_conditional_edges("auto_setup", lambda x: "config" if x["mode"] == "code" else "menu", {"config": "config", "menu": "menu"})
workflow.add_edge("config", "generate")
workflow.add_edge("generate", "save")
workflow.add_conditional_edges("save", lambda x: x["intent"], {"success": "execute", "fail": "generate"})
workflow.add_conditional_edges("execute", lambda x: "menu" if x["retries"] == 0 or x["retries"] > 3 else "generate", {"menu": "menu", "generate": "generate"})

app = workflow.compile()

if __name__ == "__main__":
    app.invoke({"retries": 0, "selected_csvs": [], "crawl_queue": []}, {"recursion_limit": 100})
