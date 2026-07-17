# save as agent_pipeline.py
import re
from pathlib import Path

SOLUTIONS_DIR = Path("./solutions")
NOTES_DIR = Path("./notes")
MANIFEST_PATH = Path("./agent_todo.manifest")

SOLUTIONS_DIR.mkdir(exist_ok=True)
NOTES_DIR.mkdir(exist_ok=True)

def build_agent_manifest():
    # Find all code files that do not have matching markdown notes yet
    code_files = list(SOLUTIONS_DIR.glob("*.kt")) + list(SOLUTIONS_DIR.glob("*.py"))
    missing_notes = []

    for file in code_files:
        matching_note = NOTES_DIR / f"{file.stem}.md"
        if not matching_note.exists():
            missing_notes.append(file)

    if not missing_notes:
        print("✨ All clear! Your Obsidian notes match your solutions perfectly.")
        if MANIFEST_PATH.exists():
            MANIFEST_PATH.unlink()
        return

    print(f"⚠️ Found {len(missing_notes)} file(s) missing documentation notes.")
    
    manifest_content = f"""# INSTRUCTION MANIFEST FOR CODING AGENT
You are an elite software engineering agent. Your task is to process the following newly added code files and create matching study notes inside the `./notes/` folder.

## 🎯 Task Instructions:
1. For each file listed below, create a file named `./notes/<FileName>.md`.
2. Follow this precise format for each note:
   ---
   tags: [leetcode, difficulty/easy-or-medium-or-hard, ds/target-ds, pattern/target-pattern]
   difficulty: Easy | Medium | Hard
   time_complexity: O(...)
   space_complexity: O(...)
   target_language: Kotlin or Python
   ---
   # Problem Name
   ## 📋 Problem Description
   [Insert real LeetCode description text here]
   ## 🧠 Conceptual Blueprint
   [Plain English strategic explanation of the brute force vs optimal methods found in the code]
   ## ⚡ The Algorithmic Trick / Insight
   [Core breakthrough detail]
   ## 🛠️ Complete Implementations
   [Embed code snippets explicitly parsed from the source file]

3. Once all notes are generated, update the custom markdown badge values located between `<!-- START_STATS_VAL -->` and `<!-- END_STATS_VAL -->` sections in the root `./README.md` file to reflect accurate total counts.

## 📂 Target Source Files to Process:
"""
    for file in missing_notes:
        # Dynamically define the code fence syntax matching the file extension
        lang_syntax = "kotlin" if file.suffix == ".kt" else "python"
        manifest_content += f"- File Path: {file}\n  Source Code:\n```{lang_syntax}\n{file.read_text(encoding='utf-8')}\n```\n\n"

    MANIFEST_PATH.write_text(manifest_content, encoding="utf-8")
    print(f"🚀 Created agent_todo.manifest! Feed this file to your subscription agent.")

if __name__ == "__main__":
    build_agent_manifest()