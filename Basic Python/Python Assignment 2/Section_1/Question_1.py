name = input("Enter the name of the person: ")
age = int(input("Enter the age of the person: "))
marks = [0,0,0]

for i in range(3):
    marks[i] = float(input("Enter the marks of the subject: "))




sum = 0

for i in marks:
    sum = sum + i


print(f"Name of the person {name}")
print(f"Age of the person:")
print(f"Average marks are {sum/3}")