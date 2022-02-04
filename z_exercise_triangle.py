row = int(input("How many rows would you like to have: "))
direction = input("Press h for horizontal, v for vertical: ")

number = 0

if direction == "h":
    for r in range(row):
        for c in range(r+1):
            number += 1
            print(number, end=" ")
        print()

elif direction == "v":
    for r in range(row):
        number = r + 1
        increase = row - 1
        for c in range(r+1):
            print(number, end=" ")
            number = number + increase
            increase = increase - 1
        print()