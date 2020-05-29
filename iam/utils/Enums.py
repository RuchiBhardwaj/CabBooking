"""Implementation of Enums."""
from enum import  Enum

class Input(Enum):
    user_choice = "choose\n 1.Create Employee\n 2.Update Employee\n 3.Delete Employee\n 4.Add new cab\n 5.Employee bookings\n 6.Add routes\n 7.Delete routes\n 8.Exit:\n "
    invalid_choice = "Invalid choice"
    update_username = "Please enter the username for whom you want to update: "
    update_password = "Please enter the new password to be updated: "
    password_updated = "Password changed for employee"
    delete_username = "Please enter the username for whom you want to delete: "
    employee_deleted = "Employee is successfully deleted"
    cab_number = "Enter cab number: "
    capacity = "Enter cab capacity: "
    cab_added = "New cab data is added"
    emp_id = "Please enter the employee id for whom you want to see: "
    stop_name = "Enter name of stop: "
    number_of_stops = "Enter stop number: "
    time_input = 'Enter 24 hour Time format HH:MM: '
    routes_added = "Routes has been added"
    route_id = "Enter Route id of the cab: "
    user_selection = """\nAvailable functionality for the Employee are:
                       1.Book a cab
                       2.View Rides
                       3.Cancel Ride
                       4.Exit 
                        """
    action = "Select the action to be performed: "
    username = "Please enter the username : "
    password =  "Please enter the password : "
    menu  ='Welcome to cab console portal\n===========================\n||        Menu           ||\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n||  (1)Login             ||\n||  (2)Register Employee ||\n||  (3)Register Admin    ||\n||  (4)Quit              ||\n==========================='
    no_users = 'No users found with the credentials'
    login_again = 'Please login again with correct credentials'
    welcome_employee = 'Welcome employee, here is your console'
    welcome_admin = 'Welcome admin, here is your console'
    new_user_created = "New user is created"
    source = "Please enter the Source : "
    destination = "Please enter the Destination : "
    stops = "How many stops are there: "
