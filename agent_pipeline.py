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
1. For each file listed below, create a file named `./notes/<FileName>.md`.
2. Follow this precise format for each note:
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

   ## 🧠 Conceptual Blueprint
   > [!info] Strategic Design
   > [Plain English strategic explanation of the brute force vs optimal methods found in the code]

   ## ⚡ The Algorithmic Trick / Insight
   > [!tip] Optimization Breakthrough
   > [Core breakthrough detail]

   ## ⚠️ Tricky Edge Cases & Interview Pitfalls
   > [!warning] Critical Pitfalls
   > [Edge cases to watch out for, e.g., empty inputs, negatives, numeric overflow]

   ## 🛠️ Complete Implementations
   [Embed code snippets explicitly parsed from the source file]

3. Once all notes are generated, update the custom markdown badge values located between `<!-- START_STATS_VAL -->` and `<!-- END_STATS_VAL -->` sections in the root `./README.md` file to reflect accurate total counts.

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