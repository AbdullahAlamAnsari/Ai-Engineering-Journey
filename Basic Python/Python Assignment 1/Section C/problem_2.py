t = ("Ahmed","Ali","Khurram")

print(t[0])
print(t[2])

# we can't change the tuple - i used list to change it

l = list(t)

l[0] = "Arslan"

l = tuple(l)

for k in l:
    print(k)