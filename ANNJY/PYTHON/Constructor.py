class Employee:
    
    def _init_(self):
        print("Employee created.")

    def _del_(self):
        print("Destructor called,Employee deleted.")

obj = Employee()

del obj
