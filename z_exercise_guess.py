import random

number = int(input("Pick a number between 1 and 1000: "))
min = 0
max = 1000
count = 0
guess_number = random.randint(min,max)

while number != guess_number:
    count += 1
    if guess_number > number:
        print("The number that entered is smaller.")
        max = guess_number
    else:
        print("The number that entered is bigger.")
        min = guess_number
    guess_number = random.randint(min, max)

count += 1

print("The guess is correct!")
print("Found on guess ", count, ".", sep="")