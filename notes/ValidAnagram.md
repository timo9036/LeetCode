---
tags: [leetcode, difficulty/easy, ds/array, pattern/arrays-and-hashing]
difficulty: Easy
difficulty_score: 1
time_complexity: "O(n)"
space_complexity: "O(1)"
target_language: Kotlin
leetcode_url: "https://leetcode.com/problems/valid-anagram/"
---

![](https://img.shields.io/badge/LeetCode-242._Valid_Anagram-blueviolet?style=for-the-badge&logo=leetcode)
![](https://img.shields.io/badge/Difficulty-Easy-green?style=flat-square)
![](https://img.shields.io/badge/Time-O(n)-blue?style=flat-square)
![](https://img.shields.io/badge/Space-O(1)-red?style=flat-square)

# 242. Valid Anagram

## 📋 Problem Description
Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

An **Anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

### Constraints:
- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

---

## 🔍 Detailed Problem Breakdown & Intuition
> [!note] Understanding the Goal
> - **What is the Input?** You are given two strings, `s` and `t`.
> - **What is the Output?** A boolean status (`true` or `false`).
> - **What is an Anagram?** An anagram is simply a word puzzle where you rearrange the letters of one word to make another. For example, "silent" and "listen" are anagrams.
> 
> Let's analyze the examples in-depth to build intuition:
> * **Example 1: `s = "anagram"`, `t = "nagaram"`**
>   - Let's count the characters in both strings:
>     - In `s`: `'a'` appears 3 times, `'n'` appears 1 time, `'g'` appears 1 time, `'r'` appears 1 time, `'m'` appears 1 time.
>     - In `t`: `'a'` appears 3 times, `'n'` appears 1 time, `'g'` appears 1 time, `'r'` appears 1 time, `'m'` appears 1 time.
>   - Since both strings contain exactly the same letters in exactly the same frequencies, they are anagrams. The output is **`true`**.
> * **Example 2: `s = "rat"`, `t = "car"`**
>   - Let's count the characters:
>     - In `s`: `'r'` (1), `'a'` (1), `'t'` (1).
>     - In `t`: `'c'` (1), `'a'` (1), `'r'` (1).
>   - String `s` has a `'t'` but no `'c'`. String `t` has a `'c'` but no `'t'`.
>   - Because their letter counts do not match, they are not anagrams. The output is **`false`**.

---

## 🧠 Conceptual Blueprint
> [!info] Strategic Design
> To solve this problem, we can use three different strategies, each with different performance characteristics:
> 
> 1. **Sorting Approach:**
>    - **How it works:** If `s` and `t` contain exactly the same characters, sorting their characters alphabetically will produce identical results. For example, sorting both "anagram" and "nagaram" produces "aaagmnr".
>    - **Why it is slow:** Sorting takes $O(N \log N)$ time. We also have to allocate extra memory to convert the strings into character arrays.
> 
> 2. **HashMap Approach:**
>    - **How it works:** We use two HashMaps to store the character counts for `s` and `t` respectively. As we iterate through the strings, we increment character frequencies. Finally, we check if the two maps are equal.
>    - **Why it is faster:** Reading the characters takes $O(N)$ linear time. However, HashMaps have some memory overhead for storing keys and values.
> 
> 3. **Optimal Frequency Array:**
>    - **How it works:** Since the constraints specify that the strings only contain lowercase English letters, we know there are only 26 possible letters. Instead of a general HashMap, we can allocate a small integer array of size 26.
>    - **The Balancing Act:** We iterate through both strings. For each character in `s`, we add 1 to its count. For each character in `t`, we subtract 1. If the strings are anagrams, every single addition will be balanced by a subtraction, leaving the array filled with all zeros at the end.

---

## ⚡ The Algorithmic Trick / Insight
> [!tip] Optimization Breakthrough
> Subtracting the character `'a'` from any lowercase character (e.g. `'c' - 'a'`) yields a zero-indexed integer representation (e.g. `2` for `'c'`). This allows us to use a direct-access array of size 26 as an ultra-fast hash table, achieving $O(1)$ lookup and modification speeds with zero allocation overhead.

---

## ⚠️ Tricky Edge Cases & Interview Pitfalls
> [!warning] Critical Pitfalls
> - **Different Lengths:** If `s.length != t.length`, they cannot be anagrams. Always check this first to allow an $O(1)$ early return.
> - **Unicode / Large Alphabets:** If the input can contain Unicode characters (beyond lowercase English), a size-26 array will cause out-of-bounds errors. In that case, you must fall back to a HashMap.

---

## 💡 Step-by-Step Educational Deep Dive
> [!note] Beginner-Friendly Explanation
> - **Data Structures used**:
>   - **Array (IntArray)**: A fixed contiguous list of numbers. Here, we use `IntArray(26)` where each index (0 to 25) maps to letters 'a' to 'z'.
>   - **Map (MutableMap)**: Key-value stores where keys are letters and values are counts. Useful if we don't know the character set size in advance.
> - **Time & Space Analysis**:
>   - **Sorting**: Time $O(n \log n)$ because of the sorting step. Space $O(n)$ to store the character array during sort.
>   - **HashMap**: Time $O(n)$ because we read each string character once. Space $O(k)$ where $k \le 26$, which is $O(1)$ auxiliary.
>   - **Optimal Array**: Time $O(n)$ as we make one pass. Space $O(1)$ auxiliary because the array size (26) is independent of the input string length $n$.
> - **Dry Run / Walkthrough**:
>   Let's trace `s = "anagram"`, `t = "nagaram"` with the **Optimal Frequency Array**:
>   1. Initialize `count = [0, 0, 0, ..., 0]` (26 zeros).
>   2. Loop through both strings simultaneously:
>      - `i = 0`: `s[0] = 'a'` (index 0) -> `count[0]++` (1). `t[0] = 'n'` (index 13) -> `count[13]--` (-1).
>      - `i = 1`: `s[1] = 'n'` (index 13) -> `count[13]++` (0). `t[1] = 'a'` (index 0) -> `count[0]--` (0).
>      - ...
>      - By the end of the loop, all increments from `s` are balanced out by decrements from `t`.
>   3. Iterate through `count` array. All values are `0` -> returns `true`.

---

## 🛠️ Complete Implementations

### Kotlin Implementation
```kotlin
package solutions

import java.util.Arrays

class ValidAnagram {

    // Approach 1 - Sorting
    fun isAnagramSorting(s: String, t: String): Boolean {
        if (s.length != t.length) return false
        return s.toCharArray().sorted() == t.toCharArray().sorted()
    }

    // Approach 2 - HashMap
    fun isAnagramHashMap(s: String, t: String): Boolean {
        if (s.length != t.length) return false

        val countS = mutableMapOf<Char, Int>()
        val countT = mutableMapOf<Char, Int>()

        for (i in s.indices) {
            countS[s[i]] = countS.getOrDefault(s[i], 0) + 1
            countT[t[i]] = countT.getOrDefault(t[i], 0) + 1
        }
        return countS == countT
    }

    // Approach 3 - Optimal Frequency Array
    fun isAnagramOptimal(s: String, t: String): Boolean {
        if (s.length != t.length) return false

        val count = IntArray(26)
        for (i in s.indices) {
            count[s[i] - 'a']++
            count[t[i] - 'a']--
        }

        for (value in count) {
            if (value != 0) return false
        }
        return true
    }
}

fun main() {
    val solver = ValidAnagram()
    assert(solver.isAnagramOptimal("anagram", "nagaram"))
    assert(!solver.isAnagramOptimal("rat", "car"))
    println("✅ ValidAnagram tests passed!")
}
```
