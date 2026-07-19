package solutions

import java.util.HashSet

/*
 * [Single Responsibility]: Houses multiple algorithm variants to check if an array
 * contains any duplicate values. Serves as a runnable compiler validation target.
 */
class ContainsDuplicate {

    /*
     * [Approach 1 - Brute Force]: Compares every single number to every other number.
     * Time Complexity: O(n²) because of nested loops.
     * Space Complexity: O(1) because we allocate no extra memory.
     */
    fun hasDuplicateBruteForce(nums: IntArray): Boolean {
        // [Outer Loop]: Iterates through each index in the array from start to end.
        for (i in nums.indices) {
            // [Inner Loop]: Iterates through index j starting immediately after index i.
            // This avoids redundant checks and comparing an element with itself.
            for (j in i + 1 until nums.size) {
                // [Equivalence Check]: If elements at positions i and j are identical.
                if (nums[i] == nums[j]) {
                    // [Early Return]: A duplicate exists. Terminate execution and return true.
                    return true
                }
            }
        }
        // [Success Return]: Examined all pairs and found no duplicates. Return false.
        return false
    }

    /*
     * [Approach 2 - Sorting]: Sorts the numbers so duplicates are positioned adjacent to each other.
     * Time Complexity: O(n log n) due to sorting.
     * Space Complexity: O(1) or O(n) depending on the sorting algorithm implementation.
     */
    fun hasDuplicateSorting(nums: IntArray): Boolean {
        // [State Mutation]: Sorts the array elements in place in ascending order.
        nums.sort()
        // [Linear Check]: Iterates starting from index 1 to the end of the array.
        for (i in 1 until nums.size) {
            // [Adjacent Check]: Compares current element with the previous one.
            if (nums[i] == nums[i - 1]) {
                // [Early Return]: Duplicate detected side-by-side. Return true.
                return true
            }
        }
        // [Success Return]: Iterated through sorted array and found no adjacent matches. Return false.
        return false
    }

    /*
     * [Approach 3 - Optimal HashSet]: Uses a HashSet to remember elements we have already seen.
     * Time Complexity: O(n) because looking up and inserting in a HashSet takes O(1) time on average.
     * Space Complexity: O(n) since the HashSet can grow to store all elements in the worst case.
     */
    fun hasDuplicateOptimal(nums: IntArray): Boolean {
        // [Structure Allocation]: Creates a hash table representing a unique set of integers.
        val seen = HashSet<Int>()
        // [Iteration Loop]: Iterates through each number in the input array.
        for (num in nums) {
            // [Membership Query]: Instantly checks in O(1) average time if the number is already in the set.
            if (num in seen) {
                // [Early Return]: The number was previously inserted, confirming a duplicate. Return true.
                return true
            }
            // [State Insertion]: Inserts the number into the set to remember it for future iterations.
            seen.add(num)
        }
        // [Success Return]: Traversed the entire array and all numbers were unique. Return false.
        return false
    }
}

/*
 * [Main Entry Point]: Execution runner containing sample test cases with assertions.
 */
fun main() {
    // [Instance Instantiation]: Creates a new instance of the contains duplicate algorithm class.
    val solver = ContainsDuplicate()

    // [Test Data 1]: An array containing duplicates.
    val testCase1 = intArrayOf(1, 2, 3, 1)
    // [Test Data 2]: An array with all unique elements.
    val testCase2 = intArrayOf(1, 2, 3, 4)

    // [Assertion 1]: Validates brute force correctly returns true for duplicate inputs.
    assert(solver.hasDuplicateBruteForce(testCase1)) { "Test Case 1 failed on Brute Force" }
    // [Assertion 2]: Validates brute force correctly returns false for unique inputs.
    assert(!solver.hasDuplicateBruteForce(testCase2)) { "Test Case 2 failed on Brute Force" }

    // [Assertion 3]: Validates sorting correctly returns true for duplicate inputs.
    assert(solver.hasDuplicateSorting(testCase1.clone())) { "Test Case 1 failed on Sorting" }
    // [Assertion 4]: Validates sorting correctly returns false for unique inputs.
    assert(!solver.hasDuplicateSorting(testCase2.clone())) { "Test Case 2 failed on Sorting" }

    // [Assertion 5]: Validates optimal hashset correctly returns true for duplicate inputs.
    assert(solver.hasDuplicateOptimal(testCase1)) { "Test Case 1 failed on Optimal" }
    // [Assertion 6]: Validates optimal hashset correctly returns false for unique inputs.
    assert(!solver.hasDuplicateOptimal(testCase2)) { "Test Case 2 failed on Optimal" }

    // [Output Logging]: Confirms all assertions passed successfully.
    println("✅ All ContainsDuplicate assertions passed successfully!")
}