import unittest
import os
import json
import re
from pathlib import Path
from qa_agent import save_session, save_pom_files

class TestQAAgent(unittest.TestCase):
    
    def setUp(self):
        self.test_session_file = "session_state.json"
        
    def tearDown(self):
        if os.path.exists(self.test_session_file):
            os.remove(self.test_session_file)
        
    def test_save_session(self):
        state = {"website_name": "OrangeHRM", "user_instruction": "Test login", "url": "http://example.com"}
        save_session(state)
        self.assertTrue(os.path.exists(self.test_session_file))
        with open(self.test_session_file, "r") as f:
            data = json.load(f)
            self.assertEqual(data["website_name"], "OrangeHRM")
            
    def test_save_pom_files_block_format(self):
        # Test the new v5.2 Block Format parsing logic
        block_content = """
Some conversational text here.
--- FILE: pages/test_page.py ---
class TestPage:
    pass

--- FILE: tests/test_script.py ---
def test_something():
    assert True
"""
        state = {"pom_json_str": block_content}
        result = save_pom_files(state)
        
        self.assertEqual(result["execution_output"], "")
        self.assertTrue(os.path.exists("pages/test_page.py"))
        self.assertTrue(os.path.exists("tests/test_script.py"))
        
        # Verify content
        content = Path("pages/test_page.py").read_text()
        self.assertIn("class TestPage:", content)
        
        # Cleanup
        os.remove("pages/test_page.py")
        os.remove("tests/test_script.py")
        if os.path.exists("pages") and not os.listdir("pages"): os.rmdir("pages")
        if os.path.exists("tests") and not os.listdir("tests"): os.rmdir("tests")

if __name__ == '__main__':
    unittest.main()
