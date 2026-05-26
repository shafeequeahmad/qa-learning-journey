# Playwright QA Agent Walkthrough (v5.0 Enterprise Edition)

Congratulations! You now have a fully persistent, highly advanced Enterprise AI QA Architect running on your machine.

## 1. Starting & Resuming Sessions
Run the agent from your terminal:
```bash
python qa_agent.py
```
If you ever close your terminal, the Agent writes your progress to `session_state.json`. The next time you boot it up, it will say: *"Welcome back! Do you want to resume your previous project?"* and pick up exactly where you left off.

## 2. The Multi-Page CSV Shopping Cart
When you tell the Agent what to test, it will create a permanent, beautifully organized folder structure:
`/TCs/OrangeHRM/orangehrm_login_tc.csv`

When you approve a set of Test Cases, the Agent won't instantly rush to write code. It asks you if you want to **"Write more Test Cases for another page"**. 
This allows you to add `dashboard_tc.csv`, `admin_panel_tc.csv`, etc., into your "Cart" before you finally check out and generate the massive framework.

## 3. Safe Deletions & Q&A
If you type `Reject all TCs`, the Agent will physically delete that specific CSV file but **it will not exit**. It safely resets the loop so you can provide a new URL without restarting the script.
You can also chat with the Agent by asking *"What is Sanity testing?"* directly in the prompt!

## 4. Enterprise POM Framework Generation
When you finally choose to generate the code, the Agent scaffolds a masterpiece:
- **`conftest.py` & `pytest.ini`**: It automatically configures Pytest to run using Google Chrome (`--browser-channel=chrome`) in Headless mode by default.
- **Playwright Traces**: The config automatically injects `--tracing=retain-on-failure`. If a test fails, Playwright will save a `.zip` file of the exact moment it failed (API logs, DOM snapshot, network requests).
- **Advanced Testing**: The LLM injects Data-Driven `@pytest.mark.parametrize` tests, Visual Regression screenshots, and `axe-core` Accessibility validations into the Pytest files.

## 5. CI/CD & qTest Integration
The framework includes:
- A `.github/workflows/playwright.yml` file, making it instantly ready to run in the cloud on every developer Pull Request.
- A custom `utils/qtest_reporter.py` Pytest Hook. This script silently listens in the background as your tests run and prepares the API payloads to push your Pass/Fail results to a Test Management system like qTest!

## 6. The Post-Execution Loop
After the code runs, the Agent does not die. It asks: *"Execution Cycle Finished. Do you want to write TCs for remaining pages?"*
This infinite loop allows you to build out 100% test coverage for an entire application over the course of days or weeks without ever breaking your flow.
