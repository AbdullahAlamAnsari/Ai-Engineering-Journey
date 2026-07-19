# Section 3 - Q4: AI Dataset Cleaning Simulation
# Atomcamp AI18 | Python Class Activity

def clean_data(data):
    # Step 1: Calculate average of non-None values
    total = 0
    count = 0
    for val in data:
        if val is not None:
            total += val
            count += 1

    average = total // count   # integer average (as shown in example output)

    # Step 2: Replace None with average
    cleaned = []
    for val in data:
        if val is None:
            cleaned.append(average)
        else:
            cleaned.append(val)

    return cleaned


data = [23, None, 45, 67, None, 89, 12]
result = clean_data(data)
print("Original :", data)
print("Cleaned  :", result)
