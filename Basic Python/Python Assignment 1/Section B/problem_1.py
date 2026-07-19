age = int(input("Enter the age: "))


if(age<13):
    print("Child")
elif(age>=13 and age<=19):
    print("Teen")
elif(age>=20):
    print("Adult")
else:
    print("Invalid age")