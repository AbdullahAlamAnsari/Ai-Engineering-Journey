# Section 3 - Q2: Vowel Counter
# Atomcamp AI18 | Python Class Activity

def check_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count


text = input("Enter a string: ")
result = check_vowels(text)
print(f"Number of vowels in '{text}': {result}")
