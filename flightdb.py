import psycopg2
from datetime import datetime,timedelta
# import pytz
con=psycopg2.connect(host='localhost',user='postgres',password='Shri@1234',dbname='postgres')

def login(username,password=None):
    my_cursor=con.cursor()

    with my_cursor.connection:
        my_cursor.execute('select passwd from flight_user where name = %s',([username]))
        result=list(my_cursor)

    my_cursor.close()

    try:
        if result[0][0]==password:

            return('login successful')
        else:

            return('Incorrect password')
    except Exception:

        return(f'No User with Username {username} found..')



# print(login('kmkim'))

def signup(username,phone,email,password):
    my_cursor=con.cursor()
    with my_cursor.connection:
        try:
            my_cursor.execute('insert into flight_user (name,phone,email,passwd) values(%s,%s,%s,%s)',(username,int(phone),email,password))
            my_cursor.execute('''insert into test (user_) values(%s)''',[username])

            my_cursor.close()
            return 'User signup successful'
        except:

            my_cursor.close()
            return 'user already exists'
    con.commit()

    # try:
    #     return 'User signup successful'


# print(signup('nivas',9790459067,'shree@gmail.com','shreeshree'))

def reset_password(username,password):
    my_cursor=con.cursor()
    with my_cursor.connection:
        my_cursor.execute('update flight_user set passwd=%s where name=%s ',(password,username))
    con.commit()

    my_cursor.close()
    return 'Password Reset successful'
# print(reset_password('shri','shrishri'))



def search_flights(From,To,date,Class):
    my_cursor=con.cursor()
    with my_cursor.connection:
        my_cursor.execute('select * from flights where from_=%s and to_=%s and date_=%s and class_=%s',(From,To,date,Class))
        result=list(my_cursor)

    my_cursor.close()
    return result
# print(search_flights('coimbatore','chennai','2022-08-22','economy'))

def available_seats(_pnr):
    my_cursor=con.cursor()
    with my_cursor.connection:
        my_cursor.execute('select seats from flights where pnr=%s',[_pnr])
        result_seat=list(my_cursor)
    my_cursor.close()
    if result_seat[0][0]>0:
        return result_seat[0][0]
    return False
# print(available_seats('airchncbe24a'))

def seats(_pnr,status=None):
    my_cursor=con.cursor()
    # print(check)
    if status=='book':
        # with my_cursor.connection:
        my_cursor.execute('select seats from flights where pnr=%s',[_pnr])
        result_seat=list(my_cursor)
        # with my_cursor.connection:
        seats_updated=result_seat[0][0]-1
            # print(seats_updated)
        my_cursor.execute('update flights set seats=%s where pnr=%s',[seats_updated,_pnr])
                # print(seats_before_book)
        con.commit()
        my_cursor.close()
    if status=='cancel':
        # with my_cursor.connection:
        my_cursor.execute('select seats from flights where pnr=%s',[_pnr])
        result_seat=list(my_cursor)
        # with my_cursor.connection:
        seats_updated=result_seat[0][0]+1
            # print(seats_updated)
        my_cursor.execute('update flights set seats=%s where pnr=%s',[seats_updated,_pnr])
                # print(seats_before_book)
        con.commit()
        my_cursor.close()

# seats('indcbechn24a','cancel')



def book(user,_pnr,passenger,dob,mobile_no,age):
    my_cursor=con.cursor()
    with my_cursor.connection:

        my_cursor.execute('insert into tickets (user_,pnr,passenger,dob,mobile_no,age) values (%s,%s,%s,%s,%s,%s)',(user,_pnr,passenger,dob,mobile_no,age))
        # seats(_pnr,'book')
        # with my_cursor.connection:
        # my_cursor.execute('select seats from flights where pnr=%s',[_pnr])
        # result_seat=list(my_cursor)
        #     # with my_cursor.connection:
        # seats_updated=result_seat[0][0]-1
        seats(_pnr,'book')
        # my_cursor.execute('update flights set seats=%s where pnr=%s',[seats_updated,_pnr])
                # print(seats_before_book)
        con.commit()
    # con.commit()
    with my_cursor.connection:
            my_cursor.execute('select * from tickets where user_=%s and pnr=%s and passenger=%s and mobile_no=%s and age=%s ', (user, _pnr,passenger,mobile_no,age))
            result = list(my_cursor)


    my_cursor.close()
    return result


# print(book('shri','indcbechn22a','ni','2002-09-06',9393939393,21))
# print(book('shri','indcbechn22a','nivass','2002-09-06',9393939393,21))

def history(user,_booking_id=None):
    my_cursor = con.cursor()
    if _booking_id:
        with my_cursor.connection:
            my_cursor.execute('select tickets.user_,tickets.booking_id,tickets.pnr,flights.name_,flights.class_,flights.date_,flights.flight_time,tickets.passenger,tickets.cancelled from tickets join flights on tickets.pnr=flights.pnr where tickets.user_=%s and tickets.booking_id=%s', [user,_booking_id])
            result = list(my_cursor)
        my_cursor.close()
        return result
    else:
        with my_cursor.connection:
            my_cursor.execute('select tickets.user_,tickets.booking_id,tickets.pnr,flights.name_,flights.class_,flights.date_,flights.flight_time,tickets.passenger,tickets.cancelled  from tickets join flights on tickets.pnr=flights.pnr where tickets.user_=%s',[user])
            result=list(my_cursor)
        my_cursor.close()
        return result


# print(history('shri'))

def cancel(_booking_id,_pnr):
    my_cursor=con.cursor()
    with my_cursor.connection:
        my_cursor.execute('update tickets set cancelled=1 where booking_id=%s',[_booking_id])
        seats(_pnr,'cancel')
        con.commit()
    my_cursor.close()
    # print(seats(_pnr,'cancel'))
    return True



def cancel_time(_pnr):
    my_cursor=con.cursor()
    with my_cursor.connection:
        my_cursor.execute('select date_,flight_time from flights where pnr=%s',[_pnr])
        result=list(my_cursor)
    my_cursor.close()
    f_date, f_time = result[0][0], result[0][1]
    return time_check(f_date, f_time)



def time_check(f_date=None,f_time=None):
    # f_date,f_time=result[0][0],result[0][1]


    # print(f_time,f_date,type(f_date))
    curr_datetime = (datetime.now())       # current date
    curr_date= str(curr_datetime).split()[0]
    curr_date = list(str(curr_date).split('-'))
    # curr_time= datetime.now(pytz.timezone('Asia/Kolkata'))
    curr_time = datetime.now()
    curr_hours = curr_time.hour
    curr_minutes=curr_time.minute


    flight_date=list(str(f_date).split('-'))    #flight date
    f_hours, f_minutes, f_sec = map(str, str(f_time).split(':'))   #flight time

    # print(flight_date,curr_date)
    date_flag=True
    for f_d,c_d in zip(flight_date,curr_date):
        if int(f_d)-int(c_d)<0:

            return False
    if date_flag==True and f_time:
        return True
    return timedelta(hours=curr_hours, minutes=curr_minutes) < timedelta(hours=int(f_hours), minutes=int(f_minutes))



# print(cancel_time('indbancbe22a'))
#
# print(time_check('2022-08-22','00:00:00'))

def already_cancelled(_booking_id):
    my_cursor=con.cursor()
    with my_cursor.connection:
        my_cursor.execute('select cancelled from tickets where booking_id=%s',[_booking_id])
        result=list(my_cursor)
    my_cursor.close()
    return result[0][0]

# print(already_cancelled('9b1631b8-b94b-4d5a-9962-e6ed1f69f2d3') ==True)


def logout(user_,password=None):
    my_cursor=con.cursor()
    with my_cursor.connection:
        my_cursor.execute('''update test set password_= encrypt(%s,'salty','aes') where user_=%s''',[password,user_])
    con.commit()
    with my_cursor.connection:
        my_cursor.execute('''select convert_from(decrypt(password_::bytea,'salty','aes'),'SQL_ASCII'
        ) from test where user_=%s''',[user_])
    result=list(my_cursor)
    my_cursor.close()
    return result[0][0]

# print(logout('shri','shrishri'))

def already_login_check(user_):
    my_cursor=con.cursor()
    with my_cursor.connection:
        my_cursor.execute('''select convert_from(decrypt(password_::bytea,'salty','aes'),'SQL_ASCII'
        ) from test where user_=%s''',[user_])
    result=list(my_cursor)
    my_cursor.close()
    try:
        return result[0][0]
    except IndexError as e:
        return False

# print(already_login_check('nivas') is None)