class Person:
    def __init__(self, name, age, marital_status, organization_type, employee_type):
      #initialiding basic details  
        self.name = name
        self.age = age
        self.marital_status = marital_status
        self.organization_type = organization_type
        self.employee_type = employee_type

class Employee(Person):
    def __init__(self, name, age, marital_status, organization_type, employee_type, income, gis_contributions, life_insurance_premium, self_education_allowance, donations, bonus_amount, rental_income=0, dividend_income=0, other_income=0, pf_contributions=0, num_children=0, child_edu_allowances=None, sponsored_edu_expenses=None):
      #initialiding  employee details inherit it feom person 
        super().__init__(name, age, marital_status, organization_type, employee_type)
        self.income = income
        self.gis_contributions = gis_contributions
        self.life_insurance_premium = life_insurance_premium
        self.self_education_allowance = self_education_allowance
        self.donations = donations
        self.bonus_amount = bonus_amount
        self.rental_income = rental_income
        self.dividend_income = dividend_income
        self.other_income = other_income
        self.pf_contributions = pf_contributions
        self.num_children = num_children
        self.child_edu_allowances = child_edu_allowances or []
        self.sponsored_edu_expenses = sponsored_edu_expenses or []

class TaxCalculator:
    def __init__(self, employee):
        self.employee = employee

    def calculate_tax(self):
        total_income = self.employee.income

      #diduction of gis and PF contributions(those amount which will not be included in tex dectutable amount) 
        total_income -= self.employee.gis_contributions
        total_income -= self.employee.pf_contributions if self.employee.employee_type.lower() == "regular" else 0

       #renraln income (20% deduction)
        rental_income = self.employee.rental_income * 0.8
        total_income += rental_income

       # calculating dividend income   
        if self.employee.dividend_income > 30000:
            dividend_income = (self.employee.dividend_income - 30000) * 0.9
        else:
            dividend_income = self.employee.dividend_income
        total_income += dividend_income

       #calculating the other income (30% deduction)
        other_income = self.employee.other_income * 0.7
        total_income += other_income

       #deducting children education allowance and also other deduction 
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
    while True:
      # main loop to calculate the tax for multiple users.  
        print("\nPersonal Income Tax (PIT) Calculator")
        name = input("Enter your name: ")

        while True:
            try:
                age = int(input("Enter your age: "))
                if age > 100:
                    print("Enter your age correctly.") # as we know people above 100 age will not earn so they dont have to pay if if person enter more than 100 years it will ask to reenter it again.
                    continue
                break
            except ValueError:
                print("Such number doesn't exist so please enter a valid number.") # valueError like "-=87, (78;;" such number.

        if age < 18:
            # if the user is below 18 he/she dont have to pay text.
            print("Dear user You are below 18 years old so you are exempted from paying tax.")
            continue

        while True:
            marital_status = input("Enter your marital status (Married/Single): ").lower()
            if marital_status in ["married", "single"]:
                break
            else:
                print("There is no such option, make sure you check the spelling and retype it again.") #if user typet the wrong spelling

        while True:
            organization_type = input("Enter the organization type (Government/Private/Corporation): ").lower()
            if organization_type in ["government", "private","corporation"]:
                break
            else:
                print("There is no such option, make sure you check the spelling and retype it again.")  #if user typet the wrong spelling

        while True:
            employee_type = input("Enter the employee type (Regular/Contract): ").lower()
            if employee_type in ["regular", "contract"]:
                break
            else:
                print("There is no such option, make sure you check the spelling and retype it again.")  #if user typet the wrong spelling

       # collecting marritial details.( id user is single this isb not naccearry)
        num_children = 0
        child_edu_allowances = []
        sponsored_edu_expenses = []
        if marital_status == "married":
            num_children = int(input("Enter the number of your children: "))
            if num_children > 0:
                for child in range(num_children):
                    while True:
                        try:
                            allowance = float(input(f"Enter education allowance for child {child + 1} (max Nu. 350,000): "))
                            if allowance > 350000:
                                print("You crossed your limit amount, please re-enter the amount within Nu. 350,000.") 
                            else:
                                child_edu_allowances.append(allowance)
                                break
                        except ValueError:
                            print(" Such number doesn't exist, Please enter a valid number.")
                for child in range(num_children):
                    while True:
                        goes_to_school = input(f"Does your child {child + 1} go to school? (y/n): ").lower()
                        if goes_to_school in ['y', 'n']:
                            break
                        print("There is no such option, make sure you check the spelling and retype it again.")
                    
                    if goes_to_school == "y":
                        while True:
                            try:
                                expense = float(input(f"Enter your sponsored education expense for your child {child + 1} (max Nu. 350,000): "))
                                if expense > 350000:
                                    print("You crossed your limited amount, please re-enter the amount within Nu. 350,000.")
                                else:
                                    sponsored_edu_expenses.append(expense)
                                    break
                            except ValueError:
                                print("Dear user, please enter a valid number.")
                    else:
                        sponsored_edu_expenses.append(0)

        while True:
            try:
              # financial details for text deduction
                income = float(input("Enter your annual gross salary: "))
                gis_contributions = float(input("Enter your GIS contributions: "))
                life_insurance_premium = float(input("Enter your life insurance premium: "))
                self_education_allowance = float(input("Enter your self-education allowance, if any: ") or 0)
                donations = float(input("Enter your donations (if any): ") or 0)
                if donations > 0.05 * income:
                    print("You are not allowed to donate more than 5% of your total adjusted gross income. Please re-enter your donation amount.")
                    donations = float(input("Enter your donations (if any): ") or 0)
                bonus_amount = float(input("Enter your bonus amount: ") or 0)
                rental_income = float(input("Enter your annual rental income (if any): ") or 0)
                dividend_income = float(input("Enter your annual dividend income (if any): ") or 0)
                other_income = float(input("Enter your annual income from other sources (if any): ") or 0)

               # only ask for pf if the usre is regular employee 
                pf_contributions = 0
                if employee_type == "regular":
                    if organization_type == "private":
                        gets_pf = input("Do you get PF? (y/n): ").lower()
                        if gets_pf == "y":
                            pf_contributions = float(input("Enter your provident fund (PF) contributions: "))
                    else:
                        pf_contributions = float(input("Enter your provident fund (PF) contributions: "))
                
                break
            except ValueError:
                print("Please enter a valid number.")

        employee = Employee(
            name, age, marital_status, organization_type, employee_type, income, gis_contributions,
            life_insurance_premium, self_education_allowance, donations, bonus_amount, rental_income,
           
            dividend_income, other_income, pf_contributions=pf_contributions,
            num_children=num_children, child_edu_allowances=child_edu_allowances,
            sponsored_edu_expenses=sponsored_edu_expenses
        )
        tax_calculator = TaxCalculator(employee)
        tax_amount = tax_calculator.calculate_tax()
        print(f"Your tax amount is: Nu. {tax_amount:.2f}")

       #asking if they want to calculate tax for other user as well 
        another_user = input("\nDo you want to calculate the tax for another user? (y/n): ").lower()
        if another_user != "y":
            break

if __name__ == "__main__":
    main()