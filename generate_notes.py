import os
import sys
from pathlib import Path
from google import genai

# ==========================================
# CONFIGURATION SETTINGS
# ==========================================
# Replace these with the actual paths on your machine
SOLUTIONS_DIR = "./solutions" 
OBSIDIAN_VAULT_DIR = "./notes"
MODEL_NAME = "gemini-2.5-flash"

# ==========================================
# SYSTEM PROMPT ARCHITECTURE
# ==========================================
SYSTEM_PROMPT = """
You are an elite FAANG Technical Interviewer and Computer Science Professor specialized in data structures and algorithms (DSA). Your task is to analyze raw source code solutions to LeetCode problems and generate highly structured, deeply analytical Markdown files suitable for a long-term personal knowledge base.

You must strictly output the response in raw Markdown format, starting with a clean YAML frontmatter block. Do not wrap your entire output in a secondary overarching markdown block—only output the natural text.

Structure your analysis according to the following strict sections:

1. YAML FRONTMATTER
   Provide the following exactly inside the frontmatter:
   - tags: Array of strings. Must include 'leetcode', difficulty level, data structures used, and patterns (e.g., [leetcode, difficulty/easy, ds/array, pattern/arrays-and-hashing]).
   - difficulty: Easy, Medium, or Hard.
   - time_complexity: Big-O notation string.
   - space_complexity: Big-O notation string.
   - target_language: The programming language of the code file.

2. 📋 PROBLEM DESCRIPTION
   - Look up the actual LeetCode description for this problem name. Write out the core requirements and constraints clearly.

3. 🧠 CONCEPTUAL BLUEPRINT
   - Explain the operational logic of the different approaches found within the code in plain English. Keep it conversational but technically accurate.

4. ⚡ THE ALGORITHMIC TRICK / INSIGHT
   - Explicitly define the fundamental trade-off or core logic pattern that changes this problem from slow to optimal.

5. ⚠️ TRICKY EDGE CASES & INTERVIEW PITFALLS
   - Provide a bulleted list detailing scenarios that would break naive implementations and how an engineer should handle them.

6. 🛠️ COMPLETE IMPLEMENTATIONS
   - Embed the clean code provided split into logical sections using appropriate code fence blocks matching the target language. Label each section with its respective time and space complexities.
"""

def process_solution_file(filename: str):
    # Ensure directories exist
    os.makedirs(OBSIDIAN_VAULT_DIR, exist_ok=True)
    
    source_path = Path(SOLUTIONS_DIR) / filename
    if not source_path.exists():
        print(f"❌ Error: Source file not found at {source_path}")
        return

    print(f"📖 Reading target solution: {filename}...")
    with open(source_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    problem_title = source_path.stem
    target_ext = source_path.suffix.lower()
    lang_map = {".kt": "Kotlin", ".py": "Python", ".java": "Java", ".js": "JavaScript"}
    language = lang_map.get(target_ext, "Unknown")

    # Initialize the modern unified GenAI client 
    # This automatically draws from your local export GEMINI_API_KEY environment variable
    try:
        client = genai.Client()
    except Exception as e:
        print("❌ Initialization Error: Please verify that GEMINI_API_KEY is configured in your terminal environment.")
        return

    full_prompt = f"{SYSTEM_PROMPT}\n\nHere is the source code file name: {filename}\nLanguage context: {language}\n\nCode Contents:\n{code_content}"

    print(f"🤖 Generating professional study documentation via {MODEL_NAME}...")
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
        )
        
        # Clean text response
        markdown_output = response.text
        
        # Write output file straight to your local Obsidian environment
        output_file_path = Path(OBSIDIAN_VAULT_DIR) / f"{problem_title}.md"
        with open(output_file_path, "w", encoding="utf-8") as out_file:
            out_file.write(markdown_output)
            
        print(f"✅ Success! Document compiled and deployed to: {output_file_path}")
        
    except Exception as e:
        print(f"❌ Execution failed during API transaction processing: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 Usage command format: python generate_notes.py <FileName.kt>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    process_solution_file(target_file)