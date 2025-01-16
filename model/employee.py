import copy

# Define Employee class
class Employee:
    def __init__(self, name, shifts_per_week, holiday_per_week, personal_leave):
        self.set_name(name)
        self.set_shifts_per_week(shifts_per_week)
        self.set_max_holiday_per_week(holiday_per_week)
        self.set_personal_leave(personal_leave)

    def display_info(self):
        return (f"Name: {self.name}\n"
                f"Shifts per week: {', '.join(self.shifts_per_week)}\n"
                f"Holiday per week: {self.holiday_per_week}\n"
                f"Personal leave: {', '.join(self.personal_leave)}")

    def set_name(self, new_name):
        self.name = new_name

    def set_shifts_per_week(self, new_shifts):
        if isinstance(new_shifts, list) and all(isinstance(shift, str) for shift in new_shifts):
            self.shifts_per_week = copy.deepcopy(new_shifts)
        else:
            raise ValueError("Shifts per week must be a list of strings.")

    def set_max_holiday_per_week(self, new_holiday):
        if isinstance(new_holiday, int):
            self.holiday_per_week = new_holiday
        else:
            raise ValueError("Holiday per week must be an integer.")

    def set_personal_leave(self, new_personal_leave):
        if isinstance(new_personal_leave, list) and all(isinstance(leave, str) for leave in new_personal_leave):
            self.personal_leave = copy.deepcopy(new_personal_leave)
        else:
            raise ValueError("Personal leave must be a list of strings.")


