# Playwright UI Test Case Generator & Automation Agent (v3.1)

## Goal Description
Build an AI Agent that generates Test Cases (with strict visual UI checks, prioritizing CSV output), can ingest design documents, and automatically generates a Professional **Page Object Model (POM)** Pytest codebase. 

Additionally, the Agent will be **Framework-Aware**: It can seamlessly integrate new pages and tests into an existing framework if one is already present.

## Proposed Architecture Updates

### 1. Existing Framework Detection & Integration (NEW)
Before the `generate_pytest` node writes any code, the Agent will scan the `week07_ai_testcases/` directory.
- **If no framework exists:** The Agent will scaffold the entire POM architecture (`/pages`, `/tests`, `/utils`, `/constants`) from scratch.
- **If a framework exists:** The Agent will read the existing `base_page.py`, `app_constants.py`, and `common_logic.py`. It will then instruct the LLM to write the *new* `page.py` and `test.py` files using the exact same coding style, naming conventions, and shared utilities of your existing framework. It will append new constants instead of overwriting the file.

### 2. Intelligent Code Generation (POM)
- `pages/`: Stores CSS/XPATH locators. Contains `base_page.py` with strict error handling (try-except, timeouts).
- `tests/`: Scripts that strictly call Page Objects and assert Pass/Fail.
- `utils/`: Common logic.
- `constants/`: Expected visual UI texts, URLs.

### 3. CSV Formatting & Bug Reporting
- TCs outputted as `test_cases.csv`.
- Support documents (wireframes) ingested at the start to establish baselines.
- Failed tests generate `[TC_Name]_failure.md` bug reports upon request.

## User Review Required

> [!IMPORTANT]  
> The agent is now designed to be fully **Framework-Aware**. It can build from scratch or scale an existing repository. Please review this final addition. If everything is perfect, please give the final approval so I can execute the code generation!

## Verification Plan
1. Rewrite `qa_agent.py` to handle framework detection using Python's `os` and `pathlib`.
2. Run `python qa_agent.py`.
3. Provide a test URL and approve the TCs.
4. Verify the agent creates the framework from scratch.
5. Run the agent a *second* time on a different URL, and verify it correctly detects the `/pages` directory and *adds* the new tests instead of overwriting the `base_page.py`.
