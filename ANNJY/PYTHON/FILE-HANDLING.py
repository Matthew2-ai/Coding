file = open('C:/Users/HP/OneDrive/Documents/Coding/ANNJY/PYTHON/File1.txt','r')
print(file.read())
file.close()

file = open('C:/Users/HP/OneDrive/Documents/Coding/ANNJY/PYTHON/File1.txt','r')
print("/n Read in parts /n")
print(file.read(8))
file.close()

file = open('C:/Users/HP/OneDrive/Documents/Coding/ANNJY/PYTHON/File1.txt','a')
file.write("HI!,I am Matthew Adedoyin, and i am 8yrs old")
file.close()
