data = {"name" : "Abdullah","age" : 19,"course" : "computer science","Marks":200}


for i in data:
    print(f"{i} {data[i]}")

data["Marks"] = 220

print(data["Marks"])