"""Write a program that ask user to enter a radian and height to create a cylinder.  Find volume of 
cylinder. Write a program that ask user to enter a radian to create a sphere. Find the volume of the 
sphere. How many spheres can be put into cylinder.

Display the result as given format, Cylinder volume is 50 sphere volume is 8 Cylinder can contain 
sphere 6.

Hint: Be careful that radian of sphere must be smaller than radian of cylinder.

Cylinder volume : pi . r squre . h      sphere volume : 4/3 . pi. r cube.
"""

pi = 22/7                          # for cylinder
height = float(input("Please enter the height: "))
radian = float(input("Please enter the radian: "))
volume1 = pi*(radian**2)*height

radian2 = float(input("Please enter the radian: "))                         #for sphere
volume2 = (4/3) * pi * (radian2**3)

if radian<=radian2:
    print("Error! Sphere cannot put into the cylinder because of it's radius.")

elif volume1>=volume2:
    unit = int(volume1//volume2)
    print("Cylinder's volume is: ", format(volume1, ".2f"), "sphere's volume is: ", format(volume2, ".2f"), "And cylinder can contain ", unit, "spheres.")
else:
    print("Error! Volume of sphere exceeds volume of cylinder.")