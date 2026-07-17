# 🚀 LeetCode & NeetCode FAANG Preparation Engine

An automated, data-driven framework designed to master Data Structures & Algorithms (DSA), build deep syntax fluency in Kotlin and Python, and systematically prepare for technical interviews.

---

## 📊 Performance & Progress Tracker

<!-- START_STATS_VAL -->
![](https://img.shields.io/badge/Total%20Problems%20Solved-1-blueviolet?style=for-the-badge&logo=leetcode)
![](https://img.shields.io/badge/Easy-1-green?style=for-the-badge)
![](https://img.shields.io/badge/Medium-0-orange?style=for-the-badge)
![](https://img.shields.io/badge/Hard-0-red?style=for-the-badge)
<!-- END_STATS_VAL -->

### 🎯 Objective Strategy
- **Primary Language:** Kotlin (Optimizing for day-job autonomy & structured type safety in system design)
- **Curriculum Track:** NeetCode 150 Mastery Tree
- **Knowledge Base:** Synced locally with an Obsidian Markdown Vault using YAML frontmatter for deep query mapping.

---

## 📂 Repository Architecture

```text
CODE/
│
├── solutions/       # Compilable production source files (Kotlin/Python)
│   └── ContainsDuplicate.kt
│
├── notes/           # Automated Markdown study sheets synced to Obsidian Vault
│   └── ContainsDuplicate.md
│
└── generate_notes.py # Local LLM compiler engine pipeline
```

---

## ⚡ Automated Toolchain Usage

When a problem is solved locally within the `./solutions/` directory, the study matrix documentation sheet is auto-compiled via the internal generation engine:

```bash
# Execute the pipeline utility
python generate_notes.py YourProblemName.kt
```
The engine automatically evaluates the source implementation, determines time/space complexities, extracts core optimization insights, maps tricky edge cases, and deploys a fully tagged file straight to the documentation directory.
