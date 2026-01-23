class Employee:
    def __init__(self, name, emp_id, base_salary):
        self.name = name
        self.emp_id = emp_id
        self.base_salary = base_salary

    def calculate_salary(self):
        return self.base_salary

    def display_info(self):
        print(f"姓名：{self.name}，工号：{self.emp_id}，基本工资：{self.base_salary}")


class Manager(Employee):
    def __init__(self, name, emp_id, base_salary, bonus):
        super().__init__(name, emp_id, base_salary)
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.bonus

    def display_info(self):
        super().display_info()
        print(f"职位：经理，奖金：{self.bonus}，总工资：{self.calculate_salary()}")


class Developer(Employee):
    def __init__(self, name, emp_id, base_salary, programming_language):
        super().__init__(name, emp_id, base_salary)
        self.programming_language = programming_language

    def calculate_salary(self):
        return self.base_salary * 1.2

    def display_info(self):
        super().display_info()
        print(f"职位：开发人员，编程语言：{self.programming_language}，总工资：{self.calculate_salary()}")


# 测试代码
if __name__ == "__main__":
    print("=== 员工信息测试 ===")
    
    # 创建经理对象
    mgr = Manager("张经理", "M001", 8000, 3000)
    mgr.display_info()
    
    print()
    
    # 创建开发人员对象
    dev = Developer("李开发", "D001", 7000, "Python")
    dev.display_info()
    
    print()
    
    # 多态演示
    print("=== 多态演示 ===")
    employees = [mgr, dev]
    
    for emp in employees:
        emp.display_info()
        print()