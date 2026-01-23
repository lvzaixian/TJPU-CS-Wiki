class Employee:
    def __init__(self, name, emp_id, base_salary):
        self.name = name
        self.emp_id = emp_id
        self.base_salary = base_salary

    def calculate_salary(self):
        return self.base_salary

    def display_info(self):
        return f"员工: {self.name}, 工号: {self.emp_id}, 工资: {self.calculate_salary()}"


class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, bonus):
        super().__init__(name, emp_id, base_salary)
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.bonus

    def display_info(self):
        info = super().display_info()
        return f"{info}, 职位: 经理, 奖金: {self.bonus}"


class Developer(Employee):
    def __init__(self, name, emp_id, base_salary, programming_language):
        super().__init__(name, emp_id, base_salary)
        self.programming_language = programming_language

    def calculate_salary(self):
        return self.base_salary * 1.2

    def display_info(self):
        info = super().display_info()
        return f"{info}, 职位: 开发, 编程语言: {self.programming_language}"


# 测试代码
manager = Manager("张三", "M001", 10000, 5000)
developer = Developer("李四", "D001", 8000, "Python")

print(manager.display_info())
print(developer.display_info())
