from saga import SagaBuilder, SagaError
from flight import flightBookingSaga
from hotel import HotelBookingSaga
from carSaga import CarBookingSaga
import mysql.connector as mysql

src = ""
dst = ""
date = ""
name = ""
phone = ""
newName = ""
newName1 = ""
newName2 = ""
TripID = 0

def BookFlight():
    
    flg = flightBookingSaga()
    
    global src
    global dst 
    global date

    src = input("Enter source city: ")
    dst = input("Enter destination city: ")
    date = input("Enter Travel date(YYYY-MM-DD): ")

    lst = flg.getFlights(src, dst, date)
    print("List of flights: ")

    for i in range(len(lst)):
        print(lst[i])

    flightName = input("Enter FlightID to be Booked : ")    
    seats = input("Number of seats to be booked : ")

    if(flg.bookFlight(flightName, int(seats))):
        
        print("Flight Booked")
        db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor = db.cursor()
        global newName
        newName = str(flightName + name)
        fid = newName
        sql = "update data set FlightBookingID  = %s, FBStatus = %s where TripID = %s"
        cursor.execute(sql, (newName, 1, TripID))
        db.commit()
        cursor.close()
        db.close()

    else:
        raise BaseException('Flight Cannot be Booked')

def BookHotel():
    hotelObj = HotelBookingSaga()
    hlist = hotelObj.getHotel(dst, date)
    print("List of Hotels for destination city : ")

    for i in range(len(hlist)):
        print(hlist[i])

    hotelName = input("Enter Hotel Name ")
    rooms = input("Enter Number of Rooms to be booked ")
    if(hotelObj.bookHotel(hotelName, int(rooms))):
        
        print("Hotel Booked")
        db1 = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor1 = db1.cursor()
        global newName1
        newName1 = str(hotelName + name)
        hid = newName1
        sql1 = "update data set HotelBookingID  = %s, HBStatus = %s where TripID = %s"
        cursor1.execute(sql1, (newName1, 1, TripID))
        db1.commit()
        cursor1.close()
        db1.close()
    else:
        raise BaseException('Hotel Cannot be Booked')

def reg():
    
    global name
    global phone

    name = input("Enter name : ")
    phone = int(input("Enter Phone number : "))

    db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
    cursor = db.cursor()
    sql = "select * from userReg where name = %s && phone = %s"
    cursor.execute(sql, (name, phone))
    row = cursor.fetchall()
    
    if(cursor.rowcount == 0):
        
        sql = "insert into userReg (name, phone) values (%s, %s)"
        cursor.execute(sql, (name, phone))
        db.commit()
        print("New user created")
        print("Welcome user" + name + " ")

    else:
        print("Existing user")
        print("Welcome user " + row[0][0] + " ")
    
    db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
    cursor = db.cursor()
    sql = "insert into data (Name, Phone) values (%s, %s)"
    cursor.execute(sql, (name, phone))
    db.commit()
    cursor.close()
    db.close()
    
    db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
    cursor = db.cursor()
    sql = "select * from data"
    cursor.execute(sql)
    row = cursor.fetchall()
    global TripID

    TripID = cursor.rowcount
    db.commit()
    cursor.close()
    db.close()

def InsertOLTP():
    
    db3 = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
    cursor3 = db3.cursor()
    sql3 = "insert into OLTP values (%s, %s, %s, %s, %s, %s)"
    cursor3.execute(sql3, (TripID, name, phone, newName, newName1, newName2))
    db3.commit()
    cursor3.close()
    db3.close()
    print("Trip successfully created with " + str(TripID) + " TripID")

def BookCar():
    
    carS = CarBookingSaga()
    clist = carS.getCar(dst, date)
    print("List of cars for destination city : ")

    for i in range(len(clist)):
        print(clist[i])
    
    carName = input("Enter car name : ")
    cars = int(input("Enter number of cars : "))

    if(carS.bookCar(carName, cars)):
        print("Car booked")
        db2 = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor2 = db2.cursor()
        global newName2
        newName2 = str(carName + name)
        cid = newName2
        sql2 = "update data set CarBookingID  = %s, CBStatus = %s, TripPendingLock = %s, Cancellation = %s where TripID = %s"
        cursor2.execute(sql2, (newName2, 1, 0, 0, TripID))
        db2.commit()
        cursor2.close()
        db2.close()

    else:
        raise BaseException('Car Cannot be Booked')

def cancelFlight():
    
    db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
    cursor = db.cursor()
    sql = "update data set FlightBookingID  = %s, FBStatus = %s, Cancellation = %s, TripPendingLock = %s where TripID = %s"
    cursor.execute(sql, (None, 0, 1, 0, TripID))
    db.commit()
    cursor.close()
    db.close()
    print("Flight booking Cancelled")

def cancelHotel():
    
    db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
    cursor = db.cursor()
    sql = "update data set HotelBookingID  = %s, HBStatus = %s, Cancellation = %s, TripPendingLock = %s where TripID = %s"
    cursor.execute(sql, (None, 0, 1, 0, TripID))
    db.commit()
    cursor.close()
    db.close()
    print("Hotel booking Cancelled")

def cancelCar():
    
    db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
    cursor = db.cursor()
    sql = "update data set CarBookingID  = %s, CBStatus = %s, Cancellation = %s, TripPendingLock = %s where TripID = %s"
    cursor.execute(sql, (None, 0, 1, 0, TripID))
    db.commit()
    cursor.close()
    db.close()
    print("Car booking Cancelled")

try:
        reg()
        SagaBuilder \
        .create() \
        .action(lambda: BookFlight(), lambda: cancelFlight()) \
        .action(lambda: BookHotel(), lambda: cancelHotel()) \
        .action(lambda: BookCar(), lambda: cancelCar()) \
        .build() \
        .execute()
        InsertOLTP()
except SagaError as e:
    print(e)  # wraps the BaseException('some error happened')

