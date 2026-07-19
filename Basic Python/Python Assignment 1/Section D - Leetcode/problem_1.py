nums = [2, 7, 11, 15]
target = 9

seen = {}

for i in range(len(nums)):
    complement = target - nums[i]

    if complement in seen:
        print(seen[complement], i)
        break

    seen[nums[i]] = i