from employee import Employee
from menu_functions import (
    initialize_employees,
    register_employee,
    input_personal_leave,
    input_national_holidays,
    set_min_employees_per_day,
    set_max_holidays,
    change_employees_shifts,
    generate_schedule,
    display_schedule
)


# Main menu function
def menu_ui():
    while True:
        print("\nMenu:")
        print("1. Register Employee")
        print("2. Change Employee Leave Dates")
        print("3. Change Employee Shifts")
        print("4. Show Shifting Schedule")
        print("5. Set National Holidays")
        print("6. Set Minimum Employees Per Day")
        print("7. Set Max Employee Holiday Per Week")
        print("8. Initialize Employees")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "0":
            break
        elif choice == "1":
            register_employee()
        elif choice == "2":
            input_personal_leave()
        elif choice == "3":
            change_employees_shifts()
        elif choice == "4":
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year: "))
            matrixed = input("Is the schedule matrixed? (yes/no): ").strip().lower() == "yes"
            randomized = input("Should the schedule be randomized? (yes/no): ").strip().lower() == "yes"
            schedule = generate_schedule(month, year, randomized, matrixed)
            if schedule:
                display_schedule(schedule, month, year)
        elif choice == "5":
            input_national_holidays()
        elif choice == "6":
            set_min_employees_per_day()
        elif choice == "7":
            set_max_holidays()
        elif choice == "8":
            initialize_employees()
        else:
            print("Invalid choice. Please try again.")


