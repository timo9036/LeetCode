# save as generate_notes.py
import os
import sys
import re
from pathlib import Path
import requests

# ==========================================
# CONFIGURATION SETTINGS
# ==========================================
SOLUTIONS_DIR = "./solutions" 
OBSIDIAN_VAULT_DIR = "./notes"  
README_PATH = "./README.md"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Ensure directories exist
Path(SOLUTIONS_DIR).mkdir(exist_ok=True)
Path(OBSIDIAN_VAULT_DIR).mkdir(exist_ok=True)

SYSTEM_PROMPT = """
You are an elite FAANG Technical Interviewer. Analyze the raw source code solution and generate a highly structured, deeply analytical Markdown file for a personal knowledge base.
You must strictly output raw Markdown starting with a clean YAML frontmatter block. Do not wrap your response in an outer markdown code block.

Structure your analysis with these exact sections:
1. YAML FRONTMATTER (tags: [leetcode, difficulty/easy, ds/array, pattern/...], difficulty, time_complexity, space_complexity, target_language)
2. 📋 PROBLEM DESCRIPTION (Clear constraints and requirements)
3. 🧠 CONCEPTUAL BLUEPRINT (English overview of all approaches in the code)
4. ⚡ THE ALGORITHMIC TRICK / INSIGHT (The optimization breakthrough)
5. ⚠️ TRICKY EDGE CASES & INTERVIEW PITFALLS (Edge cases to watch out for)
6. 🛠️ COMPLETE IMPLEMENTATIONS (Clean code chunks wrapped in language code blocks labeled with complexities)
"""

def update_readme_stats():
    notes_dir = Path(OBSIDIAN_VAULT_DIR)
    total, easy, medium, hard = 0, 0, 0, 0
    for note_file in notes_dir.glob("*.md"):
        total += 1
        content = note_file.read_text(encoding="utf-8").lower()
        if "difficulty: easy" in content or "difficulty/easy" in content: easy += 1
        elif "difficulty: medium" in content or "difficulty/medium" in content: medium += 1
        elif "difficulty: hard" in content or "difficulty/hard" in content: hard += 1

    readme = Path(README_PATH)
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        badges = (f"![](https://img.shields.io/badge/Total%20Problems%20Solved-{total}-blueviolet?style=for-the-badge&logo=leetcode)\n"
                  f"![](https://img.shields.io/badge/Easy-{easy}-green?style=for-the-badge)\n"
                  f"![](https://img.shields.io/badge/Medium-{medium}-orange?style=for-the-badge)\n"
                  f"![](https://img.shields.io/badge/Hard-{hard}-red?style=for-the-badge)")
        updated = re.sub(r"<!-- START_STATS_VAL -->.*?<!-- END_STATS_VAL -->", f"<!-- START_STATS_VAL -->\n{badges}\n<!-- END_STATS_VAL -->", content, flags=re.DOTALL)
        readme.write_text(updated, encoding="utf-8")
        print("📈 README stats synchronized successfully!")

def generate_with_deepseek(filename: str):
    source_path = Path(SOLUTIONS_DIR) / filename
    if not source_path.exists():
        print(f"❌ Error: {source_path} not found.")
        return

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ Error: DEEPSEEK_API_KEY environment variable is missing.")
        return

    print(f"📖 Analyzing {filename} via DeepSeek...")
    code_content = source_path.read_text(encoding="utf-8")
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"File: {filename}\n\nCode:\n{code_content}"}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        markdown_output = response.json()["choices"][0]["message"]["content"]
        
        output_file = Path(OBSIDIAN_VAULT_DIR) / f"{source_path.stem}.md"
        output_file.write_text(markdown_output, encoding="utf-8")
        print(f"✅ Note deployed to: {output_file}")
        update_readme_stats()
    except Exception as e:
        print(f"❌ Transaction failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 Usage: python generate_notes.py ContainsDuplicate.kt")
        sys.exit(1)
    generate_with_deepseek(sys.argv[1])