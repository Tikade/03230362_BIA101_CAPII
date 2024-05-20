class Person:
    def __init__(self, name, age, marital_status, organization_type, employee_type):
        self.name = name
        self.age = age
        self.marital_status = marital_status
        self.organization_type = organization_type
        self.employee_type = employee_type
class Employee(Person):
    def __init__(self, name, age, marital_status, organization_type, employee_type, income, gis_contributions, life_insurance_premium, self_education_allowance, donations, bonus_amount):
        super().__init__(name, age, marital_status, organization_type, employee_type)
        self.income = income
        self.gis_contributions = gis_contributions
        self.life_insurance_premium = life_insurance_premium
        self.self_education_allowance = self_education_allowance
        self.donations = donations
        self.bonus_amount = bonus_amount
        self.num_children = 0
        self.child_edu_allowances = []
        self.sponsored_edu_expenses = []
        
        if marital_status.lower() == "married":
            self.num_children = self.get_num_children()
            if self.num_children > 0:
                self.child_edu_allowances = self.get_child_education_allowances()
                self.sponsored_edu_expenses = self.get_sponsored_education_expenses()

    def get_num_children(self):
        while True:
            try:
                return int(input("Enter the number of your children: "))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_child_education_allowances(self):
        allowances = []
        for child in range(self.num_children):
            while True:
                try:
                    allowance = float(input(f"Enter education allowance for child {child + 1} (max Nu. 350,000): "))
                    allowances.append(min(allowance, 350000))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        return allowances

    def get_sponsored_education_expenses(self):
        expenses = []
        for child in range(self.num_children):
            while True:
                goes_to_school = input(f"Does your child {child + 1} go to school? (y/n): ").lower()
                if goes_to_school in ['y', 'n']:
                    break
                print("Invalid input. Please enter 'y' or 'n'.")
            
            if goes_to_school == "y":
                while True:
                    try:
                        expense = float(input(f"Enter your sponsored education expense for your child {child + 1} (max Nu. 350,000): "))
                        expenses.append(min(expense, 350000))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
            else:
                expenses.append(0)
        return expenses
class TaxCalculator:
    def __init__(self, employee):
        self.employee = employee

    def calculate_tax(self):
        total_income = self.employee.income

        total_income -= self.employee.gis_contributions
        total_income -= self.employee.gis_contributions if self.employee.employee_type.lower() != "contract" else 0

        
        total_income -= sum(self.employee.child_edu_allowances)
        total_income -= self.employee.life_insurance_premium
        total_income -= min(self.employee.self_education_allowance, 350000)
        total_income -= min(self.employee.donations, 0.05 * total_income)
        total_income -= sum(self.employee.sponsored_edu_expenses)
        total_income -= self.employee.bonus_amount

        return self.apply_tax_slabs(total_income)

    def apply_tax_slabs(self, total_income):
        tax_amount = 0
        if total_income <= 300000:
            tax_amount = 0
        elif total_income <= 400000:
            tax_amount = (total_income - 300000) * 0.1
        elif total_income <= 650000:
            tax_amount = (total_income - 400000) * 0.15 + 10000
        elif total_income <= 1000000:
            tax_amount = (total_income - 650000) * 0.2 + 45500
        elif total_income <= 1500000:
            tax_amount = (total_income - 1000000) * 0.25 + 130500
        else:
            tax_amount = (total_income - 1500000) * 0.3 + 280500

        
        if total_income >= 1000000:
            tax_amount += tax_amount * 0.1

        return tax_amount
def main():
    print("Personal Income Tax (PIT) Calculator")
    name = input("Enter your name: ")
    while True:
        try:
            age = int(input("Enter your age: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # If age is below 18, user does not have to calculate PIT and exit the program
    if age < 18:
        print("You are below 18 years old. You are not required to pay taxes.")
        return

    marital_status = input("Enter your marital status (Married/Single): ")
    organization_type = input("Enter the organization type (Government/Private): ")
    employee_type = input("Enter the employee type (Regular/Contract): ")

    while True:
        try:
            income = float(input("Enter your annual gross salary: "))
            gis_contributions = float(input("Enter your GIS contributions: "))
            life_insurance_premium = float(input("Enter your life insurance premium: "))
            self_education_allowance = float(input("Enter your self-education allowance, if any: "))
            donations = float(input("Enter your donations (if any): "))
            bonus_amount = float(input("Enter your bonus amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    employee = Employee(name, age, marital_status, organization_type, employee_type, income, gis_contributions, life_insurance_premium, self_education_allowance, donations, bonus_amount)
    tax_calculator = TaxCalculator(employee)
    tax_amount = tax_calculator.calculate_tax()
    print(f"Your tax amount is: Nu. {tax_amount:.2f}")


if __name__ == "__main__":
    main()
