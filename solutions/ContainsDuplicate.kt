class ContainsDuplicate {

    // 1. Brute Force — Time: O(n²), Space: O(1)
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

    // 2. Sorting Approach — Time: O(n log n), Space: O(1)
    fun hasDuplicateSorting(nums: IntArray): Boolean {
        nums.sort()
        for (i in 1 until nums.size) {
            if (nums[i] == nums[i - 1]) {
                return true
            }
        }
        return false
    }

    // 3. Optimal Approach (Hash Set) — Time: O(n), Space: O(n)
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