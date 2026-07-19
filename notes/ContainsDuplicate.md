---
tags: [leetcode, difficulty/easy, ds/array, pattern/arrays-and-hashing]
difficulty: Easy
difficulty_score: 1
time_complexity: O(n)
space_complexity: O(n)
target_language: Kotlin
leetcode_url: "https://leetcode.com/problems/contains-duplicate/"
---

![](https://img.shields.io/badge/LeetCode-217._Contains_Duplicate-blueviolet?style=for-the-badge&logo=leetcode)
![](https://img.shields.io/badge/Difficulty-Easy-green?style=flat-square)
![](https://img.shields.io/badge/Time-O(n)-blue?style=flat-square)
![](https://img.shields.io/badge/Space-O(n)-red?style=flat-square)

# 217. Contains Duplicate

## 📋 Problem Description
Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

### Constraints:
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## 🔍 Detailed Problem Breakdown & Intuition
> [!note] Understanding the Goal
> - **What is the Input?** You are handed a list of numbers, represented as a primitive array `nums`.
> - **What is the Output?** A boolean status (`true` or `false`).
> - **What is a Duplicate?** A duplicate is any number that appears **2 or more times** in the input list.
> 
> Let's analyze the examples in-depth to build intuition:
> * **Example 1: `nums = [1, 2, 3, 1]`**
>   - We start reading from left to right.
>   - We see `1`. Then `2`. Then `3`.
>   - Finally, we see another `1`.
>   - Since `1` has appeared earlier in our scanning process, we have found a duplicate pair `(1, 1)`. The output must be **`true`**.
> * **Example 2: `nums = [1, 2, 3, 4]`**
>   - We read: `1`, then `2`, then `3`, then `4`.
>   - We inspect every number, and none of them repeat. Every number is completely unique.
>   - The output must be **`false`**.

---

## 🧠 Conceptual Blueprint
> [!info] Strategic Design
> When solving this problem, there are three primary strategies we can employ, moving from a slow beginner's approach to the most optimal software design:
> 
> 1. **Brute Force (Nested Loops):**
>    - **How it works:** We take the first number and compare it to every other number. Then we take the second number and compare it to every remaining number, and so on.
>    - **Why it is slow:** If the array has $N$ elements, we make roughly $N \times N = N^2$ comparisons. For an array of size $10^5$, this requires $10^{10}$ operations, which will cause a "Time Limit Exceeded" (TLE) error on LeetCode.
> 
> 2. **Sorting (Adjacent Checking):**
>    - **How it works:** We sort the array first. Sorting arranges numbers in order (e.g., `[3, 1, 2, 1]` becomes `[1, 1, 2, 3]`). Once sorted, any duplicate values are forced to stand right next to each other. We make a single scan through the array checking if `nums[i] == nums[i-1]`.
>    - **Trade-off:** Sorting takes $O(N \log N)$ time, which is much faster than brute force. It uses $O(1)$ extra space if sorted in place, but it mutates the input array.
> 
> 3. **Optimal HashSet (Tracking Memory):**
>    - **How it works:** We walk through the array and store each number we see in a "memory notebook" called a `HashSet`. Before we add a number to the notebook, we ask: *"Have we written this number down already?"*
>    - **Why it is fast:** A `HashSet` uses a hashing function to find elements in $O(1)$ average time. This means checking if a number has been seen before is instantaneous.
>    - **Trade-off:** We trade memory space to gain execution speed. We achieve a fast linear runtime $O(N)$, but allocate $O(N)$ space in memory to store the set.

---

## ⚡ The Algorithmic Trick / Insight
> [!tip] Optimization Breakthrough
> Utilizing a `HashSet` allows us to trade memory space for runtime efficiency. Checking if a value exists inside a `HashSet` takes $O(1)$ constant time on average, reducing our total execution speed down to linear time.

---

## ⚠️ Tricky Edge Cases & Interview Pitfalls
> [!warning] Critical Pitfalls
> - **Empty or Single-Element Arrays:** The constraint notes 1 <= nums.length, but always ensure your loops don't throw out-of-bounds exceptions on single-item inputs.
> - **Negative Values:** A primitive array can contain negative digits. The `HashSet` framework inherently handles negative integers correctly without extra offset transformations.

---

## 💡 Step-by-Step Educational Deep Dive
> [!note] Beginner-Friendly Explanation
> - **Data Structures used**:
>   - **HashSet**: A data structure that stores unique elements. It is backed by a hash table, which allows checking if an item exists or adding a new item in constant $O(1)$ time on average.
> - **Time & Space Analysis**:
>   - **Brute Force**: Time $O(n^2)$ because we run nested loops comparing all elements. Space $O(1)$ since no additional memory is allocated.
>   - **Sorting**: Time $O(n \log n)$ due to the sorting operation. Space $O(1)$ if sorted in place, or $O(n)$ if sorting requires copy buffers.
>   - **Optimal HashSet**: Time $O(n)$ because we iterate through the array of size $n$ exactly once, and each set lookup/insert is $O(1)$. Space $O(n)$ because in the worst case (no duplicates), we store all $n$ elements in the set.
> - **Dry Run / Walkthrough**:
>   Let's trace `nums = [1, 2, 3, 1]` with the **Optimal HashSet** approach:
>   1. Initialize `seen = HashSet()` (empty).
>   2. Loop through `nums`:
>      - `num = 1`: Is `1` in `seen`? No. Add `1` to `seen`. (`seen = {1}`)
>      - `num = 2`: Is `2` in `seen`? No. Add `2` to `seen`. (`seen = {1, 2}`)
>      - `num = 3`: Is `3` in `seen`? No. Add `3` to `seen`. (`seen = {1, 2, 3}`)
>      - `num = 1`: Is `1` in `seen`? YES! Return `true`.
>   3. The duplicate is found, returning `true` successfully.

---

## 🛠️ Complete Implementations

### Kotlin Implementation
```kotlin
package solutions

import java.util.HashSet

class ContainsDuplicate {

    // Approach 1 - Brute Force
    fun hasDuplicateBruteForce(nums: IntArray): Boolean {
        for (i in nums.indices) {
            for (j in i + 1 until nums.size) {
                if (nums[i] == nums[j]) {
                    return true
                }
            }
        }
        return false
    }

    // Approach 2 - Sorting
    fun hasDuplicateSorting(nums: IntArray): Boolean {
        nums.sort()
        for (i in 1 until nums.size) {
            if (nums[i] == nums[i - 1]) {
                return true
            }
        }
        return false
    }

    // Approach 3 - Optimal (Hash Set)
    fun hasDuplicateOptimal(nums: IntArray): Boolean {
        val seen = HashSet<Int>()
        for (num in nums) {
            if (num in seen) {
                return true
            }
            seen.add(num)
        }
        return false
    }
}

fun main() {
    val solver = ContainsDuplicate()
    val testCase1 = intArrayOf(1, 2, 3, 1)
    val testCase2 = intArrayOf(1, 2, 3, 4)
    assert(solver.hasDuplicateOptimal(testCase1))
    assert(!solver.hasDuplicateOptimal(testCase2))
    println("✅ ContainsDuplicate tests passed!")
}
```