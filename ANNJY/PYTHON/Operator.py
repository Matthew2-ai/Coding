with open('File1.txt', 'w') as file:
    file.write("Hi  i am Matthew Adedoyin")
    file.close()

with open('File1.txt', 'r') as file:
    data = file.readlines()
    print("Words in the file are ...........")
    for line in data
    word = line.split()
    print(word)
file.close()
