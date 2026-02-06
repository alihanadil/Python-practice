class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary
    def total_salary(self):
        return int(self.base_salary)
class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent
    def total_salary(self):
        return int(self.base_salary) * (1 + int(self.bonus_percent)/100)
class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects
    def total_salary(self):
        return int(self.base_salary) + int(self.completed_projects) * 500
class Intern(Employee):
    def __init__(self, name, base_salary):
        super().__init__(name, base_salary)
n = input().split()
if (n[0] == "Manager"):
    emp = Manager(n[1],n[2],n[3])
    sal = emp.total_salary()
    print(f"Name: {emp.name}, Total: {sal:.2f}")
elif (n[0] == "Developer"):
    emp = Developer(n[1],n[2],n[3])
    sal = emp.total_salary()
    print(f"Name: {emp.name}, Total: {sal:.2f}")
else:
    emp = Intern(n[1], n[2])
    sal = emp.total_salary()
    print(f"Name: {emp.name}, Total: {sal:.2f}")