---
tags: [leetcode, difficulty/easy, ds/array, pattern/arrays-and-hashing]
difficulty: Easy
time_complexity: O(n)
space_complexity: O(n)
target_language: Kotlin
---
# 217. Contains Duplicate

## 📋 Problem Description
Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

## 🧠 Conceptual Blueprint
- **Brute Force:** Compare every single number to every other number using nested loops. If a match is found, return true.[cite: 2]
- **Sorting:** Sort the array first. If there are duplicates, they are forced to stand right next to each other. We check adjacent elements in a single linear pass.[cite: 2]
- **Optimal:** We iterate through the array once while maintaining a memory tracker (`HashSet`). For each item, we perform an instantaneous check to see if we've encountered it before. If yes, we stop early.[cite: 2]

## ⚡ The Algorithmic Trick / Insight
Utilizing a `HashSet` allows us to trade memory space for runtime efficiency. Checking if a value exists inside a `HashSet` takes O(1) constant time on average, reducing our total execution speed down to linear time.[cite: 2]

## ⚠️ Tricky Edge Cases & Interview Pitfalls
- **Empty or Single-Element Arrays:** The constraint notes 1 <= nums.length, but always ensure your loops don't throw out-of-bounds exceptions on single-item inputs.
- **Negative Values:** A primitive array can contain negative digits. The `HashSet` framework inherently handles negative integers correctly without extra offset transformations.[cite: 2]

## 🛠️ Complete Implementations

### Approach 1: Brute Force
- **Time Complexity:** O(n^2)
- **Space Complexity:** O(1)
```kotlin
fun hasDuplicateBruteForce(nums: IntArray): Boolean {
    for (i in nums.indices) {
        for (j in i + 1 until nums.size) {
            if (nums[i] == nums[j]) return true
        }
    }
    return false
}
```

### Approach 2: Sorting
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(1) (Auxiliary)
```kotlin
fun hasDuplicateSorting(nums: IntArray): Boolean {
    nums.sort()
    for (i in 1 until nums.size) {
        if (nums[i] == nums[i - 1]) return true
    }
    return false
}
```

### Approach 3: Optimal (Hash Set)
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)
```kotlin
fun hasDuplicateOptimal(nums: IntArray): Boolean {
    val seen = HashSet<Int>()
    for (num in nums) {
        if (num in seen) return true
        seen.add(num)
    }
    return false
}
```