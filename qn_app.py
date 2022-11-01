from flightdb import login,signup,reset_password,search_flights,book,history,available_seats,cancel,cancel_time,time_check,already_cancelled,logout,already_login_check
from User import user
import sys,datetime,re,questionary

class app():
    def __init__(self):
        self.user=None
        questionary.text('''**********************************\nWELCOME TO AIRLINE TICKET RESERVATION SERVICE\n************************************\n''').ask()

        self.initialise()

    def initialise(self):
        if self.user:
            questionary.text(f'user {self.user.username} already logged in').ask()

            return self._start()
        else:
            ls = questionary.select(
                "What do you want to do?",
                choices=['login', 'newuser?Signup', 'quit'],
            ).ask()


            if  ls =='login':
                obj=self.login_main()
                self.user=obj

                questionary.text('user login successful').ask()

                return self._start()
            elif ls =='newuser?Signup':
                user_obj=self.signup_main()
                self.user=user_obj
                self._start()
            elif ls =='quit':
                self._quit()


    def login_main(self):
        username=questionary.text("What is your Username ?").ask()
        if username=='':
            questionary.text('Username cannot be null').ask()
            self.login_main()
        if login(username)==f'No User with Username {username} found..':
            print(f'No User with Username {username} found..')
            self.initialise()
        login_passed=already_login_check(username)
        if login_passed is None:   #no password stored in test table
            password = questionary.password("Enter your password").ask()

            login_result = login(username, password)
            if login_result== 'login successful':

                self.user_obj=user(username,password)
                return self.user_obj

            elif login_result == 'Incorrect password':


                ls= questionary.select(
                    "What do you want to do?",
                    choices=['try again','reset password'],
                ).ask()

                if ls == 'try again':
                    self.login_main()
                elif ls  == 'reset password':
                    self.reset_main(username)
                # else:
                #     print('Please enter a valid choice')
                #     self.login_main()
            else:
                questionary.text(login_result).ask()
                # print(login_result)       MAAAAAAAAAAAAAAAAAAAAAAYYYYYYYYYYYYYY ERROR
                self.initialise()
        else:
            self.user_obj= user(username,login_passed)
            self.user=self.user_obj
            return self.initialise()

    def reset_main(self,username):
        reset=questionary.confirm("Do you want to RESET your PASSWORD?").ask()
        if reset:
            new_password = questionary.password("What's your password?").ask()

            confirm_pass= questionary.confirm(f"Confirm password {new_password}?").ask()

            if confirm_pass:
                questionary.text(reset_password(username, new_password)).ask()
                # print(reset_password(username, new_password))       MAYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY

                ls = questionary.select(
                    "What do you want to do?",
                    choices=['login','quit'],
                ).ask()

                if ls == 'quit':
                    self._quit_or_login()
                if ls == 'login':
                    return self.login_main()

            if not confirm_pass:
                questionary.text('---PASSWORD RESET NOT SUCCESSFUL---').ask()

                self.initialise()
        else:
            self.initialise()


    def _quit_or_login(self):
        ls = questionary.confirm("Are you sure want to quit?").ask()
        if not ls:
            questionary.text('Login-->').ask()

            return self.login_main()
        if ls:
            sys.exit()


    def signup_main(self):
        username = questionary.text("What is your Username ?").ask()

        while True:
            ideal_phone=r'\b[0-9]{10}\b'
            phone=questionary.text("What is your Phone Number ?").ask()
            if (re.fullmatch(ideal_phone,phone)):
                p=map(int,phone)
                if list(p)[0]!=0:
                    break

        while True:
            ideal_email= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email = questionary.text("What is your Email ?").ask()
            if (re.fullmatch(ideal_email, email)):
                break
        while True:
            password = questionary.password("Set up your password with minimum size of 5 characters").ask()
            confirm_pass = questionary.confirm(f"Confirm password {password}?").ask()
            if confirm_pass and len(password)>=5:
                break
            elif not confirm_pass or len(password<5):
                password = questionary.password("Set up your password with minimum size of 5 characters").ask()



        result=(signup(username, phone, email, password))
        if result=='user already exists':
            questionary.text('Try a different username').ask()

            self.signup_main()
        else:
            questionary.text('Try login-->').ask()

            return self.login_main()


    def _start(self):
        ls = questionary.select(
            "What do you want to do?",
            choices=['search flights','booking history','quit','logout'],
        ).ask()

        if ls == 'search flights':
            self.flights()
        if ls == 'booking history':
            self.booking_history()
        if ls == 'quit':
            logout(self.user.username,self.user.password)
            self._quit()
        if ls == 'logout':

            self.logout_main()


    def logout_main(self):
        questionary.text("You are about to logout").ask()
        ls = questionary.confirm("Do you want to logout ?").ask()

        if not ls:
            self._start()
        if ls :
            logout(self.user.username)
            questionary.text('You are logged out').ask()

            ls = questionary.select(
                "What do you want to do?",
                choices=['login','quit'],
            ).ask()

            if ls == 'login':
                return self.login_main()
            if ls == 'quit':
                return self._quit()

    def _quit(self):
        ls = questionary.confirm("Do you want to exit ?").ask()
        if not ls:
            self._start()
        if ls :
            sys.exit()

    def flights(self):

        From = questionary.text("Where do you want to board from?").ask()
        To = questionary.text("Which is your destination ?").ask()
        if From.lower()==To.lower():
            questionary.text('''Departure and Destination can not be same
            Reenter From & To again''').ask()
            self.flights()
        while True:
            date = questionary.text("When is your date of departure(yyyy-mm-dd) ?").ask()
            if re.search(r'\d{4}-\d{2}-\d{2}',str(date)):
                break
        if time_check(date,'00:00:00') is False:
            questionary.text('You cannot book on this date\nchoose subsequent dates').ask()
            self.flights()

        Class = questionary.select("What do you want to do?",choices=['economy', 'business'],).ask()

        flights = search_flights(From, To, date, Class)
        if flights:
            questionary.text('---------------------').ask()

        for flight in flights:
            questionary.text(f'Flight:{flight[0]}\nSeats available:{flight[4]}').ask()

            questionary.text('---------------------').ask()

        ls=questionary.select("What do you want to do?",choices=['Book tickets', 'Back to menu'],).ask()
        if ls == 'Book tickets':
            return self.book_tickets(flights)
        if ls == 'Back to menu':
            return self._start()



    def book_tickets(self,flights,unavailable_count=0):
        if unavailable_count==len(flights):
            questionary.text('''No flights currently available to book
            Please visit the nearby dates... 
            THANK YOU!''').ask()
            return self._start()

        for idx, flight in enumerate(flights):
            questionary.text(f'''{idx + 1}, {flight[0]}, 'price per ticket=3500''').ask()


        while True:
            try:
                flight_choice=int(input('Choose trip'))
                if flight_choice in range(1,len(flights)+1):
                    break
            except ValueError:
                questionary.text('Enter a valid input').ask()

        if available_seats(flights[flight_choice-1][6]):
            while True:
                passenger=questionary.text('What is the passenger name ?').ask()
                if passenger.isalpha():
                    break

            while True:
                dob = questionary.text('''What is the passenger's Date of birth ?''').ask()

                if re.search(r'\d{4}-\d{2}-\d{2}', dob):
                    p_year,p_month,p_date=[int(x) for x in dob.split('-')]
                    if datetime.date(p_year,p_month,p_date)<datetime.date.today():
                        break

            while True:
                ideal_phone = r'\b[0-9]{10}\b'
                mobile_no = questionary.text('''What is the passenger's mobile number ?''').ask()
                if (re.fullmatch(ideal_phone, mobile_no)):
                    p = map(int, mobile_no)
                    if list(p)[0] != 0:
                        break
            age = int((datetime.date.today() - datetime.date(p_year,p_month,p_date)).days / 365.2425)

            ticket_booked=book(self.user.username,flights[flight_choice-1][6],passenger,dob,mobile_no,age)
        else:
            questionary.text('---seats unavailable---\nNo more booking allowed. Choose a different flight').ask()

            unavailable_count += 1
            return self.book_tickets(flights,unavailable_count)
        Choice=questionary.confirm("Booked Ticket successfully\nDo you want to display ticket?").ask()
        if Choice:
            self.booking_history(ticket_booked[0][1])
        else:
            return self._start()


    def booking_history(self, _booking_id=None):
        if _booking_id:
            tickets = history(self.user.username, _booking_id)
        else:
            tickets = history(self.user.username)

        for idx, ticket in enumerate(tickets):
            status = 'Active'
            if ticket[8] == 1:
                status = 'Cancelled'
            questionary.text(f'''{idx+1} Booked by:{ticket[0]}\n  Booking ID:{ticket[1]}\n  Ticket Status:{status}\n  Flight:{ticket[2]}\n  Airline:{ticket[3]}\n  Class:{ticket[4]}\n  Passenger:{ticket[7]}\n  Date-of-Departure:{ticket[5]}\n  Time-of-flight:{ticket[6]}''').ask()

        self.post_ticket_display()


    def post_ticket_display(self, tickets=None):
        ls = questionary.select(
            "What do you want to do?",
            choices=['cancel ticket', 'menu', 'quit'],
        ).ask()



        if ls == 'cancel ticket':
            tickets = history(self.user.username)
            self.cancel_ticket()
        if ls == 'menu':
            return self._start()
        if ls == 'quit':
            self._quit()


    def cancel_ticket(self):
        tickets = history(self.user.username)
        for idx, ticket in enumerate(tickets):

            if ticket[8] == 1:
                status = 'Cancelled'
                questionary.text(
                  f'''{idx + 1} .Booked by:{ticket[0]}\n  Booking ID:{ticket[1]}\n  Status:{status}\n  Flight:{ticket[2]}\n  Passenger:{ticket[7]}''').ask()
            elif cancel_time(ticket[2]) is False:
                status='Expired'
                questionary.text(
                    f'''{idx + 1} .Booked by:{ticket[0]}\n  Booking ID:{ticket[1]}\n  Status:{status}\n  Flight:{ticket[2]}\n  Passenger:{ticket[7]}''').ask()
            else:
                status = 'Active'
                questionary.text(
                    f'''{idx + 1} .Booked by:{ticket[0]}\n  Booking ID:{ticket[1]}\n  Status:{status}\n  Flight:{ticket[2]}\n  Passenger:{ticket[7]}''').ask()



        if len(tickets) < 1:
            questionary.text('You have no tickets').ask()
            return self._start()

        while True:
            try:
                ticket_choice = int(input('Choose the ticket to cancel :'))
                if ticket_choice in range(1, len(tickets) + 1):
                    break
            except ValueError :
                questionary.text('Enter a valid input').ask()

        if already_cancelled(tickets[ticket_choice - 1][1]) == True:


            choice = questionary.confirm('''Ticket Cancelled already
                                Do you want to cancel any other ticket?''').ask()

            if choice:
                return self.cancel_ticket()
            else:
                return self._start()

        if cancel_time(tickets[ticket_choice - 1][2]) is False:  # cancel_time False so return to start means cancellation window over
            questionary.text('''Booking cancellation not possible
            Cancellation window closed.. ''').ask()

            return self._start()
        cancel_confirm=questionary.confirm('Do you want to cancel your ticket? Make sure').ask()

        if cancel_confirm:
            result = cancel(tickets[ticket_choice - 1][1], tickets[ticket_choice - 1][2])
            if result:
                questionary.text(f'Booking with booking id {tickets[ticket_choice - 1][1]} cancelled. Processing Refund..').ask()

        return self._start()



flight_app=app()
flight_app


































