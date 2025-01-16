import random
import calendar
import copy
from collections import Counter
from employee import Employee
from util import generate_weekly_list

# Global variables
employees = []
national_holidays = []
prioritized_shifts = []
min_employees_per_day = 1
max_holidays = 2
shifts = []


# Function to initialize employees
def initialize_employees():
    global employees, shifts, prioritized_shifts, max_holidays
    num_employees = int(input("Enter the number of employees: "))
    shifts_per_week = input("Enter shifts per week for each employees (comma-separated): ").replace(" ","").split(",")
    holiday_per_week = int(input("Enter holidays per week for all employees: "))
    for i in range(1, num_employees + 1):
        name = f"Employee {i}"
        personal_leave = input(f"Enter personal leave days (comma-separated) for {name}: ").replace(" ","").split(",")
        employee = Employee(name, shifts_per_week, holiday_per_week, personal_leave)
        employees.append(employee)
        
    prioritized_shifts = get_prioritized_shift(shifts_per_week)
    shifts = list(set(shifts_per_week))
    max_holidays = holiday_per_week
        

# Function to register employee
def register_employee():
    global employees, shifts, prioritized_shifts, max_holidays
    while True:
        name = input("Enter employee name (or 0 to go back): ")
        if name == "0":
            break
        holiday_per_week = input("Enter how many days in a week " + name + " get holiday: ")
        shifts_per_week = input("Enter shifts per week for " + name + " (comma-separated): ").replace(" ","").split(",")
        personal_leave = input("Enter personal leave dates (comma-separated, e.g., 1,2,3): ").replace(" ","").split(",")
        employee = Employee(name, shifts_per_week, holiday_per_week, personal_leave)
        employees.append(employee)
        shifts += shifts_per_week
        
    prioritized_shifts = get_prioritized_shift(shifts_per_week)
    shifts = list(set(shifts_per_week))
    max_holidays = holiday_per_week
        

# Function to input personal leave dates
def input_personal_leave():
    global employees
    while True:
        name = input("Enter employee name for P-leave (or 0 to go back): ")
        if name == "0":
            break
        if name not in [emp.name for emp in employees]:
            print("Employee not found. Please register the employee first.")
            continue
        dates = input("Enter P-leave dates (comma-separated, e.g., 1,2,3): ")
        for emp in employees:
            if emp.name == name:
                emp.set_personal_leave([date.strip() for date in dates.split(",")])

# Function to input national holidays
def input_national_holidays():
    global national_holidays
    while True:
        date = input("Enter N-holiday date (dd-mm, or 0 to go back): ")
        if date == "0":
            break
        day, month = map(int, date.split("-"))
        national_holidays.append((day, month))

# Function to set minimum employees per day
def set_min_employees_per_day():
    global min_employees_per_day
    min_employees_per_day = int(input("Enter minimum number of employees per day: "))

# Function to set maximum holidays for all employees
def set_max_holidays():
    global max_holidays, employees
    max_holidays = int(input("Enter maximum number of holidays for all employees: "))
    for emp in employees:
        emp.set_max_holiday_per_week(max_holidays)

# Function to initialize shifts
def change_employees_shifts():
    global shifts, employees, prioritized_shifts
    while True:
        name = input("Enter employee name for P-leave (or 0 to go back): ")
        if name == "0":
            break
        if name not in [emp.name for emp in employees]:
            print("Employee not found. Please register the employee first.")
            continue
        shifts_per_week = input("Enter shifts per week for " + name + " (comma-separated): ").replace(" ","").split(",")
        for emp in employees:
            if emp.name == name:
                emp.set_shifts_per_week(shifts_per_week)
                
    prioritized_shifts = get_prioritized_shift(shifts_per_week)
    shifts = list(set(shifts_per_week))

#generate sequential list 1 to 7
def generate_weekly_list(start, end):
    start = start % 7
    end = end % 7
    if start <= end:
        return list(range(start, end + 1))
    else:
        return list(range(start, 7)) + list(range(0, end + 1))

def get_prioritized_shift(shifts):
    shift_counts = Counter(shifts)
    min_frequency = min(shift_counts.values())
    
    return [shift for shift in shifts if shift_counts[shift] == min_frequency]
    
# Function to generate shifting schedule
def generate_schedule(month, year, randomized=True, matrixed=True):
    global max_holidays, min_employees_per_day, national_holidays, employees, prioritized_shifts
    
    schedule = []

    # Get the number of days in the month and the first weekday of the month
    num_days = calendar.monthrange(year, month)[1]
    first_weekday = calendar.monthrange(year, month)[0]

    # Generate schedule for each week
    holiday_start_options = [5,4,3,2,1,0,6]
    if randomized:
        random.shuffle(holiday_start_options)
        
    for week in range((num_days + first_weekday + 6) // 7):
        employee_holidays = {}
        employee_schedule = {}
        matrixed_schedule = {}
        week_schedule = []
        #Init
        for i, emp in enumerate(employees):
            holiday_start = holiday_start_options[i]
            employee_holidays[emp] = generate_weekly_list(holiday_start, (holiday_start + max_holidays - 1)) if max_holidays != 0 else [-1]
            employee_schedule[emp] = copy.deepcopy(emp.shifts_per_week)
            matrixed_schedule[emp] = (["Holiday"] * (max_holidays if max_holidays != 0 else 2)) + employee_schedule[emp]
        
        for day in range(7):
            current_day = week * 7 + day - first_weekday + 1
            # Fill Empty
            if current_day < 1 or current_day > num_days:
                week_schedule.append([""] * len(employees))
                continue
                
            day_schedule = [""] * len(employees)
            available_employees = employees

            # Mark national holidays
            if (current_day, month) in national_holidays:
                for emp in available_employees:
                    day_schedule[employees.index(emp)] = "N-holiday"
            available_employees = [emp for emp in available_employees if not day_schedule[employees.index(emp)]]

            # non matrix
            if matrixed:
                for i, emp in enumerate(available_employees):
                    day_schedule[employees.index(emp)] = matrixed_schedule[emp][(holiday_start_options[i] + current_day )% 7]
            else:
                # Assign holidays
                holidays = []
                for emp in available_employees:
                    emp_index = employees.index(emp)
                    day_of_week = (first_weekday + current_day - 1) % 7
                
                    if max_holidays != 0 and current_day % 7 in employee_holidays[emp]:
                        day_schedule[emp_index] = "N-holiday" if (current_day, month) in national_holidays else "Holiday"
                        # employee_holidays[emp].remove(current_day % 7)
                    elif max_holidays == 0 and day_of_week in [5, 6]:
                        day_schedule[emp_index] = "N-holiday" if (current_day, month) in national_holidays else "Holiday"
                        holidays.append((current_day, month))
                
                # Mark personal leaves
                for emp in available_employees:
                    if str(current_day) in emp.personal_leave:
                        if (current_day, month) in (national_holidays + holidays) or current_day % 7 in employee_holidays[emp]:
                            day_schedule[employees.index(emp)] = "W-leave"
                        else:    
                            day_schedule[employees.index(emp)] = "P-leave"
                available_employees = [emp for emp in available_employees if not day_schedule[employees.index(emp)]]
                
                if len(available_employees) < min_employees_per_day and (current_day, month) not in (national_holidays + holidays):
                    print(f"Not enough employees available for day {current_day}.")
                    return
                
                # Assign Shifts
                # print(current_day)
                # print("-------------------------------------------------------------------------")
                remaining_shifts = [shift for shift in shifts if shift not in prioritized_shifts]
                random_shifts = random.sample(remaining_shifts, len(remaining_shifts)) if randomized else remaining_shifts
                daily_shifts = prioritized_shifts + random_shifts
                daily_remaning_shifts = copy.deepcopy(daily_shifts)
                    
                for emp in available_employees:
                    if len(daily_shifts) == 0: break
                    emp_index = employees.index(emp)
                    emp_schedule = employee_schedule[emp]
                    # print(emp.name)
                    for shift in daily_shifts:
                        # print(shift)
                        if shift in emp_schedule:
                            # print(shift)
                            emp_schedule.remove(shift)
                            daily_shifts.remove(shift)
                            day_schedule[emp_index] = shift
                            break
            
                remaining_employees = [emp for emp in available_employees if not day_schedule[employees.index(emp)]]
                daily_remaning_shifts.reverse()
                for emp in remaining_employees:
                    emp_index = employees.index(emp)
                    emp_schedule = employee_schedule[emp]
                    # print(emp.name)
                    for shift in daily_remaning_shifts:
                        # print(shift)
                        if shift in emp_schedule:
                            # print(shift)
                            emp_schedule.remove(shift)
                            day_schedule[emp_index] = shift
                            break
             
            week_schedule.append(day_schedule)
        schedule.append(week_schedule)

    return schedule

# Function to display schedule
def display_schedule(schedule, month, year):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Get the first day of the month and the number of days in the month
    first_day_of_month, num_days_in_month = calendar.monthrange(year, month)
    
    for week_num, week in enumerate(schedule):
        print(f"\nWeek {week_num + 1} of {calendar.month_name[month]} {year}")
        
        # Print header row
        header_row = "{:<15}".format("Employee Name")
        for i, day in enumerate(days):
            # Calculate the date for the current day
            date = (week_num * 7 + i + 1) - first_day_of_month
            if 1 <= date <= num_days_in_month:
                header_row += "{:<15}".format(f"{date:02d}|{day}")
            else:
                header_row += "{:<15}".format("")
        print(header_row)
        
        # Print separator row
        separator_row = "-" * len(header_row)
        print(separator_row)
        
        # Print each employee's schedule
        for emp_num, emp in enumerate(employees):
            row = "{:<15}".format(emp.name)
            for day in range(7):
                if day < len(week):
                    row += "{:<15}".format(week[day][emp_num])
                else:
                    row += "{:<15}".format("")
            print(row)

