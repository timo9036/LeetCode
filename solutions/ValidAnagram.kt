package solutions

import java.util.Arrays

/*
 * [Single Responsibility]: Houses multiple algorithm variants to check if two strings
 * are anagrams of each other. Serves as a runnable compiler validation target.
 */
class ValidAnagram {

    /*
     * [Approach 1 - Sorting]: Sorts both strings alphabetically and compares them.
     * Time Complexity: O(n log n) because sorting a string of length n takes O(n log n) time.
     * Space Complexity: O(n) because converting a string to a char array allocates new memory.
     */
    fun isAnagramSorting(s: String, t: String): Boolean {
        // [Early Exit]: If lengths are different, they cannot be anagrams.
        if (s.length != t.length) {
            // [Early Return]: Instantly return false.
            return false
        }
        // [Comparison]: Converts s to char array, sorts it, and compares with sorted t char array.
        return s.toCharArray().sorted() == t.toCharArray().sorted()
    }

    /*
     * [Approach 2 - Hash Map]: Counts character frequencies using frequency maps and compares.
     * Time Complexity: O(n) since we traverse the strings of length n once.
     * Space Complexity: O(k) where k is the number of unique characters in the strings (at most O(n)).
     */
    fun isAnagramHashMap(s: String, t: String): Boolean {
        // [Early Exit]: If lengths are different, they cannot be anagrams.
        if (s.length != t.length) {
            // [Early Return]: Instantly return false.
            return false
        }

        // [Structure Allocation]: Creates frequency map for string s characters.
        val countS = mutableMapOf<Char, Int>()
        // [Structure Allocation]: Creates frequency map for string t characters.
        val countT = mutableMapOf<Char, Int>()

        // [Linear Loop]: Iterates through indices from 0 to s.length - 1.
        for (i in s.indices) {
            // [Map Update]: Increments the frequency count for character at s[i].
            countS[s[i]] = countS.getOrDefault(s[i], 0) + 1
            // [Map Update]: Increments the frequency count for character at t[i].
            countT[t[i]] = countT.getOrDefault(t[i], 0) + 1
        }
        // [Map Equivalence]: Returns true if both maps contain identical key-value entries.
        return countS == countT
    }

    /*
     * [Approach 3 - Optimal Frequency Array]: Uses a fixed-size integer array to track char offsets.
     * Time Complexity: O(n) since we iterate through the strings of length n once.
     * Space Complexity: O(1) because the frequency array size is fixed at 26 (constant memory).
     */
    fun isAnagramOptimal(s: String, t: String): Boolean {
        // [Early Exit]: If lengths are different, they cannot be anagrams.
        if (s.length != t.length) {
            // [Early Return]: Instantly return false.
            return false
        }

        // [Structure Allocation]: Allocates a fixed 26-element array representing lowercase English alphabet.
        val count = IntArray(26)
        // [Linear Loop]: Iterates through the indices of string s.
        for (i in s.indices) {
            // [Frequency Increment]: Maps s[i] to index 0-25 by subtracting 'a' character value, and increments.
            count[s[i] - 'a']++
            // [Frequency Decrement]: Maps t[i] to index 0-25 by subtracting 'a' character value, and decrements.
            count[t[i] - 'a']--
        }

        // [Validation Loop]: Iterates through each value inside the frequency tracker array.
        for (value in count) {
            // [Check Balanced]: If any count is non-zero, character frequencies do not balance out.
            if (value != 0) {
                // [Fail Return]: Mismatch detected. Return false.
                return false
            }
        }
        // [Success Return]: All character counts balanced back to zero. Return true.
        return true
    }
}

/*
 * [Main Entry Point]: Execution runner containing sample test cases with assertions.
 */
fun main() {
    // [Instance Instantiation]: Creates a new instance of the ValidAnagram solver.
    val solver = ValidAnagram()

    // [Test Data 1]: Valid anagram pair.
    val s1 = "anagram"
    val t1 = "nagaram"
    // [Test Data 2]: Invalid anagram pair.
    val s2 = "rat"
    val t2 = "car"

    // [Assertion 1]: Validates sorting method correctly returns true for anagrams.
    assert(solver.isAnagramSorting(s1, t1)) { "Test Case 1 failed on Sorting" }
    // [Assertion 2]: Validates sorting method correctly returns false for non-anagrams.
    assert(!solver.isAnagramSorting(s2, t2)) { "Test Case 2 failed on Sorting" }

    // [Assertion 3]: Validates HashMap method correctly returns true for anagrams.
    assert(solver.isAnagramHashMap(s1, t1)) { "Test Case 1 failed on HashMap" }
    // [Assertion 4]: Validates HashMap method correctly returns false for non-anagrams.
    assert(!solver.isAnagramHashMap(s2, t2)) { "Test Case 2 failed on HashMap" }

    // [Assertion 5]: Validates optimal array method correctly returns true for anagrams.
    assert(solver.isAnagramOptimal(s1, t1)) { "Test Case 1 failed on Optimal" }
    // [Assertion 6]: Validates optimal array method correctly returns false for non-anagrams.
    assert(!solver.isAnagramOptimal(s2, t2)) { "Test Case 2 failed on Optimal" }

    // [Output Logging]: Confirms all assertions passed successfully.
    println("✅ All ValidAnagram assertions passed successfully!")
}