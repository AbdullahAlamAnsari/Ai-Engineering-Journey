nums = [1,1,2]

i = 0

for j in range(1, len(nums)):
    if nums[j] != nums[i]:
        i = i + 1
        nums[i] = nums[j]

print("New Length =", i + 1)
print(nums[:i+1])