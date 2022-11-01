# from flightdb import login,signup,reset_password,search_flights,book,history,available_seats,cancel,cancel_time,time_check,already_cancelled,logout,already_login_check
from User import *
from flightdb import *
import sys,datetime,re

class app():
    def __init__(self):
        self.user=None
        self.initialise()



    def initialise(self):
        if self.user:
            print(f'user {self.user.username} already logged in')
            return self._start()
        else:
            stages=['login',
                    'newuser?Signup','quit']
            for idx,stage in enumerate(stages):
                print(idx+1,stage)
            try:
                ls=int(input('Enter choice: '))
            except :
                print('Enter only choice between 1 and 3')
                self.initialise()
            if  ls in range(len(stages)+1) and stages[ls-1]=='login':
                obj=self.login_main()

                # print(obj)    #maaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaayyyyyyyyyyyyyyyyyyy   user not instantiated
                self.user=obj

                # self.user.username=obj.username
                # self.user.password=obj.password
                # print(f'Logged in as {self.user.username}')
                print('user login successful')
                return self._start()
            elif ls in range(len(stages)+1) and stages[ls-1]=='newuser?Signup':
                user_obj=self.signup_main()
                self.user=user_obj
                self._start()
            elif ls in range(len(stages)+1) and stages[ls-1]=='quit':
                self._quit()
            else:
                print('Please enter a valid choice')
                self.initialise()


    def login_main(self):
        username = input('Enter Username: ').strip()
        if username=='':
            print('Username cannot be null')
            self.login_main()
        if login(username)==f'No User with Username {username} found..':
            print(f'No User with Username {username} found..')
            self.signup_main()

        login_passed=already_login_check(username)
        if login_passed is None:   #no password stored in test table
            password = input('Enter Password:')

            login_result = login(username, password)
            if login_result== 'login successful':
                user_obj=user(username,password)
                return user_obj

            elif login_result == 'Incorrect password':
                stages=['try again','reset password']
                print()
                for idx,stage in enumerate(stages):
                    print(idx + 1, stage)

                while True:
                    try:
                        ls = int(input('Enter choice: '))
                        if re.findall('[1-2]', str(ls)):
                            break
                    except ValueError:
                        print('Enter either 1 or 2')
                if ls in range(len(stages)+1) and stages[ls - 1] == 'try again':
                    self.login_main()
                elif ls in range(len(stages)+1) and stages[ls - 1] == 'reset password':
                    self.reset_main(username)
                else:
                    print('Please enter a valid choice')
                    self.login_main()
            else:
                print(login_result)
                self.initialise()
        else:
            user_obj= user(username,login_passed)
            self.user=user_obj
            return self.initialise()



    def reset_main(self,username):
        reset = input('Reset? Enter "YES"')
        if reset == 'YES' or reset == 'yes':
            new_password = input('Enter New Password:')
            count = 0
            while count < 2:
                count += 1
                new_p = input('Re-Enter password:')
                if new_password == new_p:
                    print(reset_password(username, new_password))
                    stages=['login','quit']
                    for idx,stage in enumerate(stages):
                        print(idx+1,stage)
                    ls=int(input('What do you want ?'))
                    if ls in range(len(stages) + 1) and stages[ls - 1] == 'quit':
                        self._quit_or_login()
                    if ls in range(len(stages) + 1) and stages[ls - 1] == 'login':
                        return self.login_main()

                if count == 2 and new_p != new_password:
                    print('---PASSWORD RESET NOT SUCCESSFUL---')
                    self.initialise()
        else:
            self.initialise()

    def _quit_or_login(self):
        stages = ['sure?', 'no']
        print('You are about to exit')
        for idx, stage in enumerate(stages):
            print(idx + 1, stage)
        ls = int(input('Choose sure to exit'))
        if ls in range(len(stages) + 1) and stages[ls - 1] == 'no':
            print('Login-->')
            return self.login_main()
        if ls in range(len(stages) + 1) and stages[ls - 1] == 'sure?':
            sys.exit()


    def signup_main(self):
        username = input('Enter Username: ').strip()
        # num_label=phone=0
        # num_label=True

        while True:
            ideal_phone=r'\b[0-9]{10}\b'
            phone=input('Enter Phone Number: ')
            if (re.fullmatch(ideal_phone,phone)):
                p=map(int,phone)
                if list(p)[0]!=0:
                    break

        while True:
            ideal_email= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email = input('Enter email:')
            if (re.fullmatch(ideal_email, email)):
                break
        while True:
            password = input('Setup New password:')
            if len(password)>=5:
                break
        while True:
            p = input('Re-Enter password:')
            if p==password:
                break
        if password == p:
            result=(signup(username, phone, email, password))
            if result=='user already exists':
                print('Try a different username')
                self.signup_main()
            else:
                print('Try login-->')
                return self.login_main()


    def _start(self,user_=None,password=None):
        menu=['search flights','booking history','quit','logout']
        for idx, item in enumerate(menu):
            print(idx + 1, item)
        # ideal_menu=r'\b[1-4]{1}\b'
        while True:
            try:
                ls = int(input('Navigate to page:'))
                if re.findall('[1-4]', str(ls)):
                    break
            except ValueError:
                print('You can enter only a choice between 1 and 4')


        if ls in range(len(menu) + 1) and menu[ls - 1] == 'search flights':
            self.flights()
        if ls in range(len(menu) + 1) and menu[ls - 1] == 'booking history':
            self.booking_history()
        if ls in range(len(menu) + 1) and menu[ls - 1] == 'quit':
            logout(self.user.username,self.user.password)
            self._quit()
        if ls in range(len(menu) + 1) and menu[ls - 1] == 'logout':
            # sys.exit()
            self.logout_main()
        # if not ls in range(len(menu)+1):
        #     print('Enter a choice only between 1 and 4')
        #     self._start()

    def logout_main(self):
        stages = ['sure?', 'no']
        print('You are about to logout')
        for idx, stage in enumerate(stages):
            print(idx + 1, stage)

        while True:
            try:
                ls = int(input('Choose sure to logout'))
                if re.findall('[1-2]', str(ls)):
                    break
            except ValueError:
                print('Enter either 1 or 2')

        if ls in range(len(stages) + 1) and stages[ls - 1] == 'no':
            self._start()
        if ls in range(len(stages) + 1) and stages[ls - 1] == 'sure?':
            logout(self.user.username)
            actions=['login','quit']
            print('You are logged out')
            for idx, action in enumerate(actions):
                print(idx + 1, action)
            ls = int(input('What do you want to do?'))
            if ls in range(len(actions) + 1) and actions[ls - 1] == 'login':
                return self.login_main()
            if ls in range(len(actions) + 1) and actions[ls - 1] == 'quit':
                return self._quit()



    def _quit(self):
        stages = ['sure?', 'no']
        print('You are about to exit')
        for idx, stage in enumerate(stages):
            print(idx + 1, stage)
        while True:
            try:
                ls = int(input('Choose sure to exit'))
                if re.findall('[1-2]', str(ls)):
                    break
            except ValueError:
                print('Enter either 1 or 2')
        if ls in range(len(stages) + 1) and stages[ls - 1] == 'no':
            self._start()
        if ls in range(len(stages) + 1) and stages[ls - 1] == 'sure?':
            sys.exit()


    def flights(self):
        From = input('From: ')
        To = input('To:')
        if From.lower()==To.lower():
            print('''Departure and Destination can not be same
            Reenter From & To again''')
            self.flights()
        while True:
            date = input('Date of departure(yyyy-mm-dd): ')
            if re.search(r'\d{4}-\d{2}-\d{2}',date):
                break
        if time_check(str(date),'00:00:00') is False:
            print('You cannot book on this date\nchoose subsequent dates')
            self.flights()
        while True:
            try:
                Class_input = int(input('Class Category(\n1.economy\n2.business) : '))
                if re.findall('[1-2]', str(Class_input)):
                    break
            except ValueError:
                print('Enter either 1 or 2')

        if Class_input==1: Class='economy'
        else: Class='business'


        flights = search_flights(From, To, date, Class)
        if flights:
            print('---------------------')
        for flight in flights:
            # print(flight)
            print(f'Flight:{flight[0]}\nSeats available:{flight[4]}')
            print('---------------------')
        stages = ['Book tickets', 'Back to menu']
        for idx, stage in enumerate(stages):
            print(idx + 1, stage)

        while True:
            try:
                ls = int(input('What do you want to do?'))
                if ls in[1,2]:
                    break
            except ValueError:
                print('Enter either 1 or 2')

        if ls in range(len(stages) + 1) and stages[ls - 1] == 'Book tickets':
            return self.book_tickets(flights)
        if ls in range(len(stages) + 1) and stages[ls - 1] == 'Back to menu':
            return self._start()


    def book_tickets(self,flights,unavailable_count=0):
        if unavailable_count==len(flights):
            print('''No flights currently available to book
            Please visit the nearby dates... 
            THANK YOU!''')
            return self._start()

        for idx,flight in enumerate(flights):
            print(idx+1,flight[0],'price per ticket=3500')

        while True:
            try:
                flight_choice=int(input('Choose trip'))
                if flight_choice in range(1,len(flights)+1):
                    break
            except ValueError:
                print('Enter a valid input')

        if available_seats(flights[flight_choice-1][6]):
            while True:
                passenger=input('Enter passenger name:').strip()
                if passenger.isalpha():
                    break

            while True:
                dob = input('Enter Date of birth of passenger:')
                if re.search(r'\d{4}-\d{2}-\d{2}',dob):
                    p_year,p_month,p_date=[int(x) for x in dob.split('-')]
                    if datetime.date(p_year,p_month,p_date)<datetime.date.today():
                        break

            while True:
                ideal_phone = r'\b[0-9]{10}\b'
                mobile_no = input('Enter passenger mobile number:')
                if (re.fullmatch(ideal_phone, mobile_no)):
                    p = map(int, mobile_no)
                    if list(p)[0] != 0:
                        break
            age = int((datetime.date.today() - datetime.date(p_year,p_month,p_date)).days / 365.2425)


            ticket_booked=book(self.user.username,flights[flight_choice-1][6],passenger,dob,mobile_no,age)
        else:
            print('---seats unavailable---\nNo more booking allowed. Choose a different flight')
            unavailable_count += 1
            return self.book_tickets(flights,unavailable_count)
        print('Booked Ticket successfully\nDo you want to display ticket?\n1.YES\n2.NO\nplease enter choice no.')
        while True:
            try:
                Choice = int(input('Please enter:'))
                if re.findall('[1-2]', str(Choice)):
                    break
            except ValueError:
                print('Enter either 1 or 2')
        if Choice==1:
            self.booking_history(ticket_booked[0][1])
        else:
            return self._start()

    def booking_history(self,_booking_id=None):
        if _booking_id:
            tickets=history(self.user.username,_booking_id)
        else:
            tickets = history(self.user.username)

        for idx,ticket in enumerate(tickets):
            status = 'Active'
            if ticket[8] == 1:
                status = 'Cancelled'
            print(idx+1,f'''Booked by:{ticket[0]}\n  Booking ID:{ticket[1]}\n  Ticket Status:{status}\n  Flight:{ticket[2]}\n  Airline:{ticket[3]}\n  Class:{ticket[4]}\n  Passenger:{ticket[7]}\n  Date-of-Departure:{ticket[5]}\n  Time-of-flight:{ticket[6]}''')
        self.post_ticket_display()


    def post_ticket_display(self,tickets=None):
        print('What do you want to do?')
        menu = ['cancel ticket', 'menu', 'quit']
        for idx, item in enumerate(menu):

            print(idx + 1, item)

        while True:
            try:
                ls = int(input('Please enter: '))
                if re.findall('[1-3]', str(ls)):
                    break
            except ValueError:
                print('Enter a choice between 1 and 3')

        if ls in range(len(menu) + 1) and menu[ls - 1] == 'cancel ticket':
            tickets=history(self.user.username)
            self.cancel_ticket()
        if ls in range(len(menu) + 1) and menu[ls - 1] == 'menu':
            return self._start()
        if ls in range(len(menu) + 1) and menu[ls - 1] == 'quit':
            self._quit()
    def cancel_ticket(self):
        tickets = history(self.user.username)
        for idx, ticket in enumerate(tickets):

            status = 'Active'
            if ticket[8]==1:
                status='Cancelled'
            elif cancel_time(ticket[2]) is False:
                status='Expired'
            print(idx + 1,f'''Booked by:{ticket[0]}\n  Booking ID:{ticket[1]}\n  Status:{status}\n  Flight:{ticket[2]}\n  Passenger:{ticket[7]}''')


        if len(tickets)<1:
            print('You have no tickets')
            return self._start()

        while True:
            try:
                ticket_choice=int(input('Choose the ticket to cancel :'))
                if ticket_choice in range(1,len(tickets)+1):
                    break
            except ValueError as e:
                print('Enter a valid input')

        if already_cancelled(tickets[ticket_choice-1][1]) ==True:

            choices=[1,2]
            while True:
                try:
                    choice = int(input('''Ticket Cancelled already
                                Do you want to cancel any other ticket?
                                1.Yes
                                2.No,exit cancel '''))
                    if re.findall('[1-2]', str(choice)):
                        break
                except ValueError:
                    print('Enter either 1 or 2')

            if choice in range(len(choices)+1) and choice==1:
                return self.cancel_ticket()
            if choice in range(len(choices)+1) and choice==2:
                return self._start()

        if cancel_time(tickets[ticket_choice-1][2]) is False:  #cancel_time False so return to start means cancellation window over
            print('''Booking cancellation not possible
            Cancellation window closed.. ''')
            return self._start()

        while True:
            try:
                cancel_confirm = int(input('''Proceed to cancel\n1.Yes\n2.No\nPlease make sure your choice'''))
                if re.findall('[1-3]', str(cancel_confirm)):
                    break
            except ValueError:
                print('Enter either 1 or 2')
        if cancel_confirm == 1:
            result=cancel(tickets[ticket_choice-1][1],tickets[ticket_choice-1][2])
            if result:
                print(f'Booking with booking id {tickets[ticket_choice-1][1]} cancelled. Processing Refund..')
        return self._start()



flight_app=app()
flight_app
# flight_app._start()
# flight_app.cancel_ticket()