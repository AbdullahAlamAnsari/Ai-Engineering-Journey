messages = []
message = input("Enter the message: ")
messages.append(message)

spam_keywords = ["free", "win"]
for message in messages:
    message_lower = message.lower()
    is_spam = False

    for keyword in spam_keywords:
        if keyword in message_lower:
            is_spam = True
            break

    print("Spam" if is_spam else "Not Spam")