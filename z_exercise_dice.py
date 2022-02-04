"""
A program to simulate several rolls of two dice. While the user wants to roll the dice:
Display a random number in the range of 1 through 6
Display another random number in the range of 1 through 6
Ask the user if they want to roll the dice again
Show the number of double rolls and double incidence percentage
"""

# This program simulates the rolling of dice.
import random

# Constants for the minimum and maximum random numbers.
MIN = 1
MAX = 6
how_many_times = 0

def main():
    # Create a variable to control the loop.
    again = "y"
    how_many_times = 0
    rounds = 0
    #Simulate rolling the dice.
    while again == "y" or again == "Y":
        print("Rolling the dice...")
        result1 = random.randint(MIN,MAX)
        result2 = random.randint(MIN,MAX)
        print("Their values are: ", result1, result2)
        
        if result1 == result2:
            how_many_times += 1

        # Do another roll of the dice?
        again = input("Roll them again? (y = yes): ")
        rounds += 1
        
    percentage = (how_many_times/rounds)*100
    print("Number of double rolls of dice:", how_many_times)
    print("Double incidence percentage: %", percentage, sep="")

main()