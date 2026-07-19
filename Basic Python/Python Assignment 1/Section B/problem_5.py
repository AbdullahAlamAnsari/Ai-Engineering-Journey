num = int(input("Enter a number: "))


if(num%5 == 0 and num%3 == 0):
    print("Num is div by both 3 and 5")
elif(num%3 == 0):
    print("Num is div by 3")
elif(num%5 == 0):
    print("Num is div by 5")
else:
    print("Num is neither div by 5 nor 3")