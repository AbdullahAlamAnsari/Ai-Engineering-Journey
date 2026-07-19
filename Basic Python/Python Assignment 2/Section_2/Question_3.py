nums = [12, 7, 18, 5, 9, 20]


count = 0
sum = 0

for k in nums:
    if(k>10):
        count += 1
    print(k)
    sum = sum + k

print(f"Total sum : {sum}")
print(f"Total number greater than 10: {count}")