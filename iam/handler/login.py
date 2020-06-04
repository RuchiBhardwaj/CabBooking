"""Implementation of the login class."""
from iam.handler.admin import Admin
from iam.handler.employee import Employee
from iam.utils.models import User
from iam.utils.models import db_url
from sqlalchemy import create_engine
from iam.handler.crypt import encrypt_message, decrypt_message
from sqlalchemy.orm import sessionmaker
from iam.handler.utilities import Register
from iam.utils.Enums import Input

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()


class main:
    def choice_input(self, db):
        """
        Function to take user input.
        """
        choice = input(">>> ").lstrip()
        return choice

    def login(self, db):
        """
        Login functionality and employee validation.
        """
        print('Welcome to Cab booking Login')
        uname = input(Input.username.value)
        passwd = input(Input.password.value)
        result = session.query(User).filter_by(username=uname)
        if result.first() is None:
            print(Input.no_users.value)
            print(Input.login_again.value)
            exit()

        for row in result:
            if decrypt_message(row.password.encode()) == passwd:
                if row.type == 'employee':
                    print(Input.welcome_employee.value)
                    Employee(row.emp_id).selection()

                elif row.type == 'admin':
                    print(Input.welcome_admin.value)
                    Admin().selection()
            else:
                print('incorrect password')

    def login_master(self, db):
        """
        Implementation of the menu.
        """
        while True:
            print(Input.menu.value)
            choice = main().choice_input(db)
            switcher = {
                '1': 'main().Login(db)',
                '2': 'Register().newUser("employee")',
                '3': 'Register().newUser("admin")',
                '4': 'exit()'
            }
            eval(switcher.get(choice, "print('Invalid choice')"))

