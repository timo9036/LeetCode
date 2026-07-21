# 🎯 Algorithmic Mastery Control Panel

---

## 📊 Solved Problems Matrix
*Track problem metrics, languages, and interview confidence scores.*

```dataview
TABLE 
    difficulty AS "Difficulty", 
    time_complexity AS "Time", 
    space_complexity AS "Space",
    confidence AS "Confidence (1-5)",
    status AS "Status",
    target_language AS "Language",
    leetcode_url AS "Problem Link"
FROM "notes"
SORT difficulty_score ASC, confidence ASC
```

---

## ⚠️ Problems Needing Review
*Identifies problems where your confidence score is low (<= 3) or marked as "Needs Review".*

```dataview
TABLE 
    difficulty AS "Difficulty", 
    confidence AS "Confidence", 
    status AS "Status", 
    last_reviewed AS "Last Reviewed"
FROM "notes"
WHERE confidence <= 3 OR status = "Needs Review" OR status = "Unsolved"
SORT last_reviewed ASC
```