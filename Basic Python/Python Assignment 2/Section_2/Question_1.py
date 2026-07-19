num = int(input("Enter the number: "))
if(num%2 == 0):
    print("Even number")
    if(num>0):
        print("Positive")
    elif(num<0):
        print("Negative")
    else:
        print("Zero")
else:
    print("Odd number")
    if(num>0):
        print("Positive")
    elif(num<0):
        print("Negative")
    else:
        print("Zero")

