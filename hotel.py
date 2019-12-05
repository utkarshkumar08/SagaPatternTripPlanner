import mysql.connector as mysql


class HotelBookingSaga(object):

    def getHotel(self, dst, date):
        db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor = db.cursor()
        sql = "select HotelName from hotellist where City = %s && Date = %s"
        cursor.execute(sql, (dst, date))
        row = cursor.fetchall()
        lst = []
        for i in row:
            lst.append(i[0])

        cursor.close()
        db.close()
        return lst


    def bookHotel(self, HotelName, rooms):

        db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor = db.cursor()
        sql = "select RoomCount from hotellist where HotelName = %s"
        cursor.execute(sql, (HotelName,))
        row = cursor.fetchall()

        if(row[0][0] >= int(rooms)):
            print("Connecting to payment gateway...")
            print("Payment Successful")
            k = abs(row[0][0] - int(rooms))
            sql = "update hotellist set RoomCount = %s where HotelName = %s"
            cursor.execute(sql,(k, HotelName))
            db.commit()
            cursor.close()
            db.close()
            return True

        else:
            #print("Seats not available for specified flights !")
            return False

