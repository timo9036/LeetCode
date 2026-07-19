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

# [Single Responsibility]: Prompts the LLM to refactor solution source code to be
# fully runnable, consolidated into a single class, and verbosely commented.
REFACTOR_PROMPT = """
You are an elite software engineering compiler-assistant. Your task is to refactor the user's LeetCode code file to be fully runnable, clean, and extremely educational for a beginner.

Follow these strict refactoring rules:
1. Consolidate multiple duplicate classes (such as multiple `class Solution` declarations in the same file) into a single descriptive class representing the problem name (e.g. `class ValidAnagram`).
2. Implement the different algorithmic approaches as descriptively named methods within that single class (e.g. `hasDuplicateBruteForce()`, `hasDuplicateSorting()`, `hasDuplicateOptimal()`).
3. Add a complete, compilable `fun main()` (for Kotlin/Java) or `if __name__ == "__main__":` (for Python) entry point that instantiates the class, runs several assertion test cases (printing inputs, outputs, and 'SUCCESS' messages), making the file fully executable.
4. Add verbose, educational, step-by-step inline comments explaining exactly what every single line of code does, the data structures used, and why they exist.
5. Return ONLY the clean refactored code. Do not wrap the response in markdown code blocks. Do not explain anything outside the code.
"""

# [Single Responsibility]: Prompts the LLM with formatting rules aligned with agent_pipeline.py.
# Standardizes Obsidian tags, visual shields badges, and native markdown callouts.
SYSTEM_PROMPT = """
You are an elite FAANG Technical Interviewer. Analyze the raw source code solution and generate a highly structured, deeply analytical Markdown file for a personal knowledge base.
You must strictly output raw Markdown starting with a clean YAML frontmatter block. Do not wrap your response in an outer markdown code block.

Structure your analysis with these exact sections and formatting:
1. YAML FRONTMATTER
   ---
   tags: [leetcode, difficulty/easy-or-medium-or-hard, ds/target-ds, pattern/target-pattern]
   difficulty: Easy | Medium | Hard
   difficulty_score: 1 | 2 | 3
   time_complexity: "O(...)"
   space_complexity: "O(...)"
   target_language: Kotlin | Python | Java
   leetcode_url: "https://leetcode.com/problems/problem-name-kebab-case/"
   ---

2. SHIELDS.IO BADGES (immediately following the YAML block, before the title):
   ![](https://img.shields.io/badge/LeetCode-<ProblemName>-blueviolet?style=for-the-badge&logo=leetcode)
   ![](https://img.shields.io/badge/Difficulty-<Easy/Medium/Hard>-<green/orange/red>?style=flat-square)
   ![](https://img.shields.io/badge/Time-O(...)-blue?style=flat-square)
   ![](https://img.shields.io/badge/Space-O(...)-red?style=flat-square)

3. # <Problem Number>. <Problem Name>

4. ## 📋 Problem Description
   [Insert real LeetCode description text here]

5. ## 🔍 Detailed Problem Breakdown & Intuition
   > [!note] Understanding the Goal
   > [Explain in plain English what the problem is asking. Detail inputs, outputs, and constraints. Walk through the sample examples step-by-step and explain verbosely why the output is what it is, mapping characters or values to illustrate the concept.]

6. ## 🧠 Conceptual Blueprint
   > [!info] Strategic Design
   > [Provide a highly verbose comparative analysis of all approaches found in the code. Explain the Brute Force approach and why its time complexity is high. Explain intermediate approaches (e.g., Sorting) and how they organize data. Finally, explain the Optimal approach, detailing why it improves speed and what trade-offs (e.g., memory vs time) are involved.]

6. ## ⚡ The Algorithmic Trick / Insight
   > [!tip] Optimization Breakthrough
   > [Core breakthrough detail]

7. ## ⚠️ Tricky Edge Cases & Interview Pitfalls
   > [!warning] Critical Pitfalls
   > [Edge cases to watch out for, e.g. empty arrays, negatives, overflow]

8. ## 💡 Step-by-Step Educational Deep Dive
   > [!note] Beginner-Friendly Explanation
   > - **Data Structures used**: [Explain why we use things like HashSets, HashMaps, or Arrays here, and what they do in simple terms]
   > - **Time & Space Analysis**: [Break down why the complexities are what they are, e.g. "Sorting takes O(n log n) because..."]
   > - **Dry Run / Walkthrough**: [Walk through a small sample input, e.g. nums = [1, 2, 3, 1], and show step-by-step how the data structures update]

9. ## 🛠️ Complete Implementations
   [Embed code snippets explicitly parsed from the source file, using proper syntax blocks, including the main runner method]
"""

def update_readme_stats():
    # [Robust State Reading]: Analyzes the Obsidian vault files to aggregate dashboard statistics.
    notes_dir = Path(OBSIDIAN_VAULT_DIR)
    total, easy, medium, hard = 0, 0, 0, 0
    for note_file in notes_dir.glob("*.md"):
        total += 1
        content = note_file.read_text(encoding="utf-8")
        
        # [Frontmatter Analysis]: Parses frontmatter boundaries to extract fields reliably.
        frontmatter_match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if frontmatter_match:
            yaml_text = frontmatter_match.group(1)
            metadata = {}
            for line in yaml_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip().lower()] = v.strip().strip('"').strip("'").lower()
            
            # [Stat Calculation]: Matches difficulty from metadata.
            difficulty = metadata.get("difficulty", "")
            if "easy" in difficulty:
                easy += 1
            elif "medium" in difficulty:
                medium += 1
            elif "hard" in difficulty:
                hard += 1

    # [State Writing]: Atomically updates Shields.io badges inside target markdown anchors.
    readme = Path(README_PATH)
    if readme.exists():
        content = readme.read_text(encoding="utf-8")
        badges = (f"![](https://img.shields.io/badge/Total%20Problems%20Solved-{total}-blueviolet?style=for-the-badge&logo=leetcode)\n"
                  f"![](https://img.shields.io/badge/Easy-{easy}-green?style=for-the-badge)\n"
                  f"![](https://img.shields.io/badge/Medium-{medium}-orange?style=for-the-badge)\n"
                  f"![](https://img.shields.io/badge/Hard-{hard}-red?style=for-the-badge)")
        updated = re.sub(
            r"<!-- START_STATS_VAL -->.*?<!-- END_STATS_VAL -->", 
            f"<!-- START_STATS_VAL -->\n{badges}\n<!-- END_STATS_VAL -->", 
            content, 
            flags=re.DOTALL
        )
        readme.write_text(updated, encoding="utf-8")
        print("📈 README stats synchronized successfully!")

def refactor_solution_file(filename: str, api_key: str) -> str:
    # [Locating Resource]: Maps file name to solutions directory.
    source_path = Path(SOLUTIONS_DIR) / filename
    if not source_path.exists():
        return ""

    code_content = source_path.read_text(encoding="utf-8")
    
    # [Idempotent Check]: Avoids duplicate API hits if main runner and comments exist.
    has_main = ("fun main" in code_content) or ("static void main" in code_content) or ("__main__" in code_content)
    if has_main:
        print(f"ℹ️ {filename} already has a main driver. Skipping automatic refactoring.")
        return code_content

    print(f"🛠️ Refactoring and adding test runner to {filename} via DeepSeek...")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": REFACTOR_PROMPT},
            {"role": "user", "content": f"File: {filename}\n\nCode:\n{code_content}"}
        ],
        "temperature": 0.1
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        refactored_code = response.json()["choices"][0]["message"]["content"].strip()
        
        # [Sanitize Code]: Strips markdown ticks if returned by LLM.
        if refactored_code.startswith("```"):
            lines = refactored_code.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            refactored_code = "\n".join(lines).strip()

        source_path.write_text(refactored_code, encoding="utf-8")
        print(f"✅ Source file updated with main runner: {source_path}")
        return refactored_code
    except Exception as e:
        print(f"⚠️ Refactoring transaction failed: {e}. Proceeding with original code.")
        return code_content

def generate_with_deepseek(filename: str):
    source_path = Path(SOLUTIONS_DIR) / filename
    if not source_path.exists():
        print(f"❌ Error: {source_path} not found.")
        return

    # [Secret Retrieval]: Reads DeepSeek API credentials from local OS environment variable.
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ Error: DEEPSEEK_API_KEY environment variable is missing.")
        return

    # [Auto-Refactoring Step]: Ensures code is runnable and fully commented before generating notes.
    code_content = refactor_solution_file(filename, api_key)

    print(f"📖 Analyzing {filename} via DeepSeek...")
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
        # [Synchronous I/O Boundary]: Executes network request to fetch AI analysis.
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        markdown_output = response.json()["choices"][0]["message"]["content"]
        
        # [Persistent Storage]: Writes the note to Obsidian Vault destination.
        output_file = Path(OBSIDIAN_VAULT_DIR) / f"{source_path.stem}.md"
        output_file.write_text(markdown_output, encoding="utf-8")
        print(f"✅ Note deployed to: {output_file}")
        update_readme_stats()
    except Exception as e:
        print(f"❌ Transaction failed: {e}")

if __name__ == "__main__":
    # [Arg Validation]: Checks input arguments. Support for --all batch processing.
    if len(sys.argv) < 2:
        print("💡 Usage: python generate_notes.py ContainsDuplicate.kt")
        print("💡 Or run: python generate_notes.py --all   (to process all missing notes)")
        sys.exit(1)
        
    if sys.argv[1] == "--all":
        # [Discovery Phase]: Finds all code files that do not have matching markdown notes yet.
        # Supports Kotlin (*.kt), Python (*.py), and Java (*.java).
        code_files = (
            list(Path(SOLUTIONS_DIR).glob("*.kt")) + 
            list(Path(SOLUTIONS_DIR).glob("*.py")) + 
            list(Path(SOLUTIONS_DIR).glob("*.java"))
        )
        missing_notes = []
        for file in code_files:
            matching_note = Path(OBSIDIAN_VAULT_DIR) / f"{file.stem}.md"
            if not matching_note.exists():
                missing_notes.append(file.name)
        
        if not missing_notes:
            print("✨ All clear! Your Obsidian notes match your solutions perfectly.")
            sys.exit(0)
            
        print(f"🔄 Discovered {len(missing_notes)} file(s) missing documentation notes.")
        for file_name in missing_notes:
            generate_with_deepseek(file_name)
    else:
        generate_with_deepseek(sys.argv[1])