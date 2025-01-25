new_file = open('New_file1.txt', 'x')
new_file.close()

import os
print("Checking if my_file exists or not")
if os.path.exists("my_file.txt"):
    os.remove("my_file.txt")

else:
    print("The file does not exist")

my_file = open("my_file.txt", 'w')
my_file.write("Hi i am Matthew Adedoyin, I am six yrs old")
my_file.close()

os.remove('New_file.txt')
os.rmdir('C:/Users/HP/OneDrive/Documents/Coding/ANNJY/PYTHON/TEST')