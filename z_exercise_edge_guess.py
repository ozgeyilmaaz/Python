"""
Define a function that gives you third unknown edge of the right-angled triangular. Design the 
algorithm starting with an introductory screen that says 'This program finds unknown edge of the 
right-angled triangle' and atter pressing 'Enter', program gives you the third edge.

Hint: You need to use Pythagorean Theorem. Hint2: You can use 'x' for unknown edge.
"""

def main():
    intro()
    lengths = []
    for i in range(1,3):
        x = int(input("Enter the edge's length: "))
        lengths.append(x)
    triangle(lengths[0], lengths[1], "x")

def intro():
    print("This program finds unknown edge of the right-angled triangle.")
    input("Press Enter.")

def triangle(opposite_edge, adjacent_edge, hypotenuse):
    if opposite_edge == str("x"):

        result = ((hypotenuse**2) - (adjacent_edge**2)) ** 0.5
        print(result)

    elif adjacent_edge == str("x"):
        result = ((hypotenuse ** 2) - (opposite_edge ** 2)) ** 0.5
        print(result)

    elif hypotenuse == str("x"):
        result = ((adjacent_edge ** 2) + (opposite_edge ** 2)) ** 0.5
        print(result)

    else:
        print("You already know all the edges.")

main()