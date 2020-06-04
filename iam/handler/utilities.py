"""Contains the functionalities invoking the database.."""
import uuid

from iam.utils.models import User, cab, routes, booking
from iam.utils.models import db_url
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy import exc

from sqlalchemy.orm import sessionmaker
from iam.handler.crypt import encrypt_message, decrypt_message
from iam.utils.Enums import Input

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()


class Register:

    def newUser(self, role):
        """
        Function to register a new user.
        """
        try:
            uname = input(Input.username.value)
            passwrd = input(Input.password.value)
            empId = str(uuid.uuid4())
            newuser = User(username=uname, password=encrypt_message(passwrd), emp_id=empId, type=role, updated_at=datetime.now(),
                           is_deleted="false")
            session.add(newuser)
            session.commit()
            print(Input.new_user_created.value)
            return True
        except exc.SQLAlchemyError as e:
            print("Error creating new employee : {}".format(e))
            return False

    def list_of_employee(self):
        """
        Function to fetch the employee details.
        """
        try:
            epm_list = session.query(User).filter_by(type="employee").filter_by(is_deleted="False").all()
            print("List of all the Employee: ")
            for row in epm_list:
                print("Username: ", row.username)
                print("Employee Id: ", row.emp_id)
                print("Password: ", row.password)
                print("Updated at: ", row.updated_at)
                print("Deleted at: ", row.deleted_at)
                print("Is Deleted: ", row.is_deleted)
                print("---------------------------")
        except exc.SQLAlchemyError as e:
            print("Error with list : {}".format(e))
            return False


    def list_of_cabs(self):
        """
        Function to fetch the list of cabs.
        """
        try:
            cab_list = session.query(cab).filter_by(is_deleted="False").all()
            print("List of all cabs")
            for row in cab_list:
                print("cab_number: ", row.cab_number)
                print("Capacity: ", row.capacity)
                print("available_seats: ", row.available_seats)
                print("------------------------------------")
        except exc.SQLAlchemyError as e:
            print("Error with list : {}".format(e))
            return False

    def list_of_routes(self):
        """
                Function to fetch the list of routes.
        """
        try:
            route_list = session.query(routes).all()
            print("List of routes")
            for row in route_list:
                print("stop_name: ", row.stop_name)
                print("route_id: ", row.route_id)
                print("----")
            session.commit()
            return True
        except exc.SQLAlchemyError as e:
            print("Error with list : {}".format(e))
            return False

    def avl_cab(self, emp_id):
        """
                Function to check the availability of cabs.
        """
        try:
            source = input(Input.source.value)
            destination = input(Input.destination.value)
            trip_time_user = input(Input.time_input.value)
            time_object_user = datetime.strptime(trip_time_user, '%H:%M').time()

            source_cabs = []
            sources = session.query(routes).filter_by(stop_name=source).filter(routes.available_seats != 0).\
                filter_by(is_deleted="False").all()

            destination_cabs = []
            destinations = session.query(routes).filter_by(stop_name=destination).filter(routes.available_seats != 0).\
                filter_by(is_deleted="False").all()

            for sor in sources:
                if datetime.strptime(sor.time, '%H:%M').time() > time_object_user:
                    avl_sour_cab = {'cab_number': sor.cab_number, 'stage_no': sor.stage, 'available_seats':
                        sor.available_seats, 'start_time': sor.time, 'route_id': sor.route_id}
                    source_cabs.append(avl_sour_cab.copy())

            for des in destinations:
                avl_dest_cabs = {'cab_number': des.cab_number, 'stage_no': des.stage, 'available_seats':
                    des.available_seats, 'route_id': des.route_id}
                destination_cabs.append(avl_dest_cabs.copy())


            total_avl_cabs = [sor['cab_number'] + "," + sor["start_time"] + "," + str(sor["available_seats"]) + "," +
                              sor['route_id'] for sor in source_cabs for des in destination_cabs if sor['cab_number']
                              == des['cab_number'] and sor['stage_no'] < des['stage_no'] and sor['route_id'] ==
                              des['route_id']]
            print("\nAvailable cabs are: ")
            avl_detail_cab = []
            for avl in total_avl_cabs:
                cab_details = avl.split(',')
                print("\ncab number: ", cab_details[0])
                print("start time: ", cab_details[1])
                print("available seats: ", cab_details[2])
                avl_detail_cab.append(cab_details)
            selected_cab = input("\nEnter the cab number to confirm the booking: ")
            self.book_cab(emp_id, selected_cab, avl_detail_cab, source, destination)
            return True

        except exc.SQLAlchemyError as e:
            print("Error while booking the cab: {}".format(e))
            return False

    def book_cab(self,emp_id, cab_num, detailed_cabs, sour, dest):
        """
        Function to book a cab.
        """
        try:
            route_id=''
            for cabs in detailed_cabs:
                if cabs[0]==cab_num:
                    route_id = cabs[3]

            destination = session.query(routes).filter_by(stop_name=dest).filter_by(cab_number=cab_num).filter_by(
                route_id=route_id).first()
            dest_stage = destination.stage
            dest_time = destination.time
            sources = session.query(routes).filter_by(stop_name=sour).filter_by(cab_number=cab_num).filter_by(
                route_id=route_id).first()
            arr_time = sources.time
            arr_stage = sources.stage
            session.query(routes).filter_by(route_id=route_id).filter(dest_stage > routes.stage).filter(
                arr_stage <= routes.stage).update({'available_seats': routes.available_seats - 1})
            new_booking_id = str(uuid.uuid4())
            new_booking = booking(booking_id=new_booking_id, emp_id=emp_id, cab_number=cab_num, source=sour,
                                  destination=dest, arrival_time=arr_time, departure_time=dest_time,
                                  created_at=datetime.now(), updated_at=datetime.now(), canceled='0')
            session.add(new_booking)
            session.commit()
            print(" cab booked successfully!")
            return True

        except exc.SQLAlchemyError as e:
            print("Error while booking the cab: {}".format(e))
            return False

    def view_rides(self, employee_id):
        try:
            self.completed_rides(employee_id)
            self.upcoming_rides(employee_id)
        except Exception as e:
            print(e)

    def upcoming_rides(self, employee_id):
        print('\nUpcoming Rides : \n')
        try:
            rides = session.query(booking).filter(booking.emp_id == employee_id).all()
            for row in rides:
                if (row.created_at.date() == datetime.now().date()) and (row.canceled == '0') \
                        and self.ride_status(row.arrival_time):
                    print('Booking ID: ', row.booking_id)
                    print('Cab_Number : ', row.cab_number)
                    print('Source : ', row.source)
                    print('Destination ; ', row.destination)
                    print('Start Time', row.arrival_time)
                    print('ETA', row.departure_time)
                    print('Cancelled', row.canceled)
        except Exception as e:
            print(e)

    def completed_rides(self, employee_id):
        print('\nCompleted Rides : \n')
        try:
            rides = session.query(booking).filter(booking.emp_id == employee_id).all()
            for row in rides:
                if (row.created_at.date() < datetime.now().date()) or not (self.ride_status(row.arrival_time)):
                    print('\nBooking ID: ', row.booking_id)
                    print('Cab_Number : ', row.cab_number)
                    print('Source : ', row.source)
                    print('Destination ; ', row.destination)
                    print('Start Time', row.arrival_time)
                    print('ETA', row.departure_time)
                    print('Cancelled', row.canceled)

        except Exception as e:
            print(e)

    def cancel_ride(self, employee_id):
        try:
            count = 0
            rides = session.query(booking).filter_by(emp_id=employee_id).all()
            for row in rides:
                if (row.created_at.date() == datetime.now().date()) and (row.canceled == '0') \
                        and self.time_diff(row.arrival_time):
                    print('\nBooking ID: ', row.booking_id)
                    print('Cab_Number : ', row.cab_number)
                    print('Source : ', row.source)
                    print('Destination ; ', row.destination)
                    print('Start Time', row.arrival_time)
                    print('ETA', row.departure_time)
                    print('Cancelled', row.canceled)
                    count += 1
            if count != 0:
                ride_id = input('Enter the booking_id you would like to cancel : ')
                session.query(booking).filter(booking.booking_id == ride_id).update({'canceled': '1'})
                session.commit()
                print('Ride Cancelled')
            else:
                print('No Upcoming Rides')
        except Exception as e:
            print(e)

    def time_diff(self, a):
        b = datetime.now()
        b = b.strftime('%H:%M')
        x = '%H:%M'
        tdelta = datetime.strptime(a, x) - datetime.strptime(b, x)
        if tdelta.days == 0 and (tdelta.seconds / 60) > 30:
            return True
        else:
            return False

    def ride_status(self, a):
        b = datetime.now()
        b = b.strftime('%H:%M')
        x = '%H:%M'
        tdelta = datetime.strptime(a, x) - datetime.strptime(b, x)
        if tdelta.days == 0 and (tdelta.seconds / 60) > 0:
            return True
        else:
            return False

