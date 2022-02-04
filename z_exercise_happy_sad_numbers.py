number_list = []

def main():
    message()
    print()
    number = int(input("Enter a number: "))
    print()
    if calculation(number):
        print("HAPPY", len(number_list))
        print("The algorithm stops at step", len(number_list), ":", number, "is a Happy number.")
    else:
        print("SAD", len(number_list))
        print("It is a loop.")
        print("The algorithm stops at step", len(number_list), ":", number, "is a Sad number.")

def calculation(x):
    sum = 0
    figures = str(x)
    for n in figures:
        sum = sum + int(n) ** 2
    if sum in number_list:
        number_list.append(sum)
        return False
    elif sum == x and len(number_list) != 0:
        number_list.append(sum)
        return False
    else:
        number_list.append(sum)
    if sum == 1:
        return True
    else:
        return calculation(sum)

def message():
    print("HAPPY-SAD NUMBERS")
    print("-----------------")
    print("This program shows whether the number entered is a happy or sad number.")
    print("And it gives the information at which step the algorithm is stopped.")

main()