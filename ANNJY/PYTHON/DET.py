class person:
    def __init__(self,fname,lname):
    self.firstname=fname
    self.lastname=lname

    def printname(self):
        print(self.firstname, self.lastname)

class Student(person):
    def __init__(self, fname, lname):
        super().__init__(fname, lname)
        self.graduationyear=year 

x=Student("MATTHEW","ADEDOYIN",2021)
x.printname()
print(x.graduationyear)