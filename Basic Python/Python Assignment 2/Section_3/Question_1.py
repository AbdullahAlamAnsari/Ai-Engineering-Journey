marks = [45, 78, 88, 32, 90, 67, 55]


passed = 0
failed = 0


for k in marks:
    if k>=50:
        passed += 1
    else:
        failed += 1


print(f"Passed no of students: {passed}")
print(f"Failed no of students: {failed}")
print(f"Maximum marks: {max(marks)}")
print(f"Minimum marks: {min(marks)}")

stats = {}

stats["passed"] = passed
stats["failed"] = failed
stats["max"]  = max(marks)
stats["min"] = min(marks)

