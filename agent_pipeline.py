# save as agent_pipeline.py
import re
from pathlib import Path

# [Single Responsibility]: Defines target directories for processing solutions, 
# generating notes, and generating the agent task manifest file.
SOLUTIONS_DIR = Path("./solutions")
NOTES_DIR = Path("./notes")
MANIFEST_PATH = Path("./agent_todo.manifest")

# [Directory Initialization]: Ensures the base structure exists before running discovery.
SOLUTIONS_DIR.mkdir(exist_ok=True)
NOTES_DIR.mkdir(exist_ok=True)

def build_agent_manifest():
    # [Multi-Language Scope]: Finds all code files that do not have matching markdown notes yet.
    # Added Java support (*.java) alongside Kotlin (*.kt) and Python (*.py).
    code_files = (
        list(SOLUTIONS_DIR.glob("*.kt")) + 
        list(SOLUTIONS_DIR.glob("*.py")) + 
        list(SOLUTIONS_DIR.glob("*.java"))
    )
    missing_notes = []

    # [Dependency Mapping]: Scans each source code file and maps it to a prospective Obsidian note.
    for file in code_files:
        # [Strict Naming]: Notes match the base name of the source code file.
        matching_note = NOTES_DIR / f"{file.stem}.md"
        # [Exclusion Logic]: Only documents files that do not currently have generated notes.
        if not matching_note.exists():
            missing_notes.append(file)

    # [Early Exit]: Prevents manifest creation if all files are documented.
    if not missing_notes:
        print("✨ All clear! Your Obsidian notes match your solutions perfectly.")
        if MANIFEST_PATH.exists():
            MANIFEST_PATH.unlink()
        return

    print(f"⚠️ Found {len(missing_notes)} file(s) missing documentation notes.")
    
    # [Cohesive Configuration]: System instructions template defining the layout structure
    # of the target Markdown notes. This aligns perfectly with generate_notes.py.
    manifest_content = """# INSTRUCTION MANIFEST FOR CODING AGENT
You are an elite software engineering agent. Your task is to process the following newly added code files and create matching study notes inside the `./notes/` folder.

## 🎯 Task Instructions:
1. Verify that each solution source file is fully compilable, runnable, and educational:
   - Consolidate multiple duplicate classes (e.g. `class Solution` defined multiple times in the same file) into a single descriptive class (e.g. `class ValidAnagram`).
   - Implement the different algorithmic approaches as descriptively named methods within that single class (e.g. `hasDuplicateBruteForce()`, `hasDuplicateSorting()`, `hasDuplicateOptimal()`).
   - Add a `fun main()` (for Kotlin/Java) or `if __name__ == "__main__":` (for Python) entry point containing test cases with assertions/prints, making the file fully executable.
   - Add verbose, step-by-step comments explaining every line of the source code.
   - If the source file lacks these, overwrite the source code file under `./solutions/<FileName>` with the corrected, commented, and runnable version.

2. For each file listed below, create a file named `./notes/<FileName>.md`.
3. Follow this precise format for each note, explaining concepts clearly for LeetCode beginners:
   ---
   tags: [leetcode, difficulty/easy-or-medium-or-hard, ds/target-ds, pattern/target-pattern]
   difficulty: Easy | Medium | Hard
   difficulty_score: 1 | 2 | 3
   time_complexity: "O(...)"
   space_complexity: "O(...)"
   target_language: Kotlin | Python | Java
   leetcode_url: "https://leetcode.com/problems/problem-name-kebab-case/"
   ---
   
   ![](https://img.shields.io/badge/LeetCode-<ProblemName>-blueviolet?style=for-the-badge&logo=leetcode)
   ![](https://img.shields.io/badge/Difficulty-<Easy/Medium/Hard>-<green/orange/red>?style=flat-square)
   ![](https://img.shields.io/badge/Time-O(...)-blue?style=flat-square)
   ![](https://img.shields.io/badge/Space-O(...)-red?style=flat-square)

   # <Problem Number>. <Problem Name>

   ## 📋 Problem Description
   [Insert real LeetCode description text here]

   ## 🔍 Detailed Problem Breakdown & Intuition
   > [!note] Understanding the Goal
   > [Explain in plain English what the problem is asking. Detail inputs, outputs, and constraints. Walk through the sample examples step-by-step and explain verbosely why the output is what it is, mapping characters or values to illustrate the concept.]

   ## 🧠 Conceptual Blueprint
   > [!info] Strategic Design
   > [Provide a highly verbose comparative analysis of all approaches found in the code. Explain the Brute Force approach and why its time complexity is high. Explain intermediate approaches (e.g., Sorting) and how they organize data. Finally, explain the Optimal approach, detailing why it improves speed and what trade-offs (e.g., memory vs time) are involved.]

   ## ⚡ The Algorithmic Trick / Insight
   > [!tip] Optimization Breakthrough
   > [Core breakthrough detail]

   ## ⚠️ Tricky Edge Cases & Interview Pitfalls
   > [!warning] Critical Pitfalls
   > [Edge cases to watch out for, e.g., empty inputs, negatives, numeric overflow]

   ## 💡 Step-by-Step Educational Deep Dive
   > [!note] Beginner-Friendly Explanation
   > - **Data Structures used**: [Explain why we use things like HashSets, HashMaps, or Arrays here, and what they do in simple terms]
   > - **Time & Space Analysis**: [Break down why the complexities are what they are, e.g. "Sorting takes O(n log n) because..."]
   > - **Dry Run / Walkthrough**: [Walk through a small sample input, e.g. nums = [1, 2, 3, 1], and show step-by-step how the data structures update]

   ## 🛠️ Complete Implementations
   [Embed code snippets explicitly parsed from the source file, including the main runner method]

4. Once all notes are generated, update the custom markdown badge values located between `<!-- START_STATS_VAL -->` and `<!-- END_STATS_VAL -->` sections in the root `./README.md` file to reflect accurate total counts.

## 📂 Target Source Files to Process:
"""
    # [Dynamic Manifest Compiling]: Iterates through each missing note file to build instructions.
    for file in missing_notes:
        # [Extension Mapping]: Derives language name for syntax highlighting based on file extension.
        if file.suffix == ".kt":
            lang_syntax = "kotlin"
        elif file.suffix == ".java":
            lang_syntax = "java"
        else:
            lang_syntax = "python"
            
        # [Manifest Append]: Reads the raw contents of each code file to supply to the workspace agent.
        manifest_content += f"- File Path: {file}\n  Source Code:\n```{lang_syntax}\n{file.read_text(encoding='utf-8')}\n```\n\n"

    # [Atomic IO Write]: Overwrites the manifest file with fresh tasks.
    MANIFEST_PATH.write_text(manifest_content, encoding="utf-8")
    print(f"🚀 Created agent_todo.manifest! Feed this file to your subscription agent.")

if __name__ == "__main__":
    build_agent_manifest()