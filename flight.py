import mysql.connector as mysql

class flightBookingSaga:

    def getFlights(self, src, dst, date):

        db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor = db.cursor()
        sql = "select * from flight where src = %s && dst = %s && dt = %s"
        cursor.execute(sql, (src, dst, date))
        row = cursor.fetchall()
        lst = []
        for i in row:
            lst.append(i[0])
        return lst
        cursor.close()
        db.close()

    def bookFlight(self, flightid, seats):

        db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor = db.cursor()
        sql = "select seatcount from flight where flightid = %s"
        cursor.execute(sql, (flightid,))
        row = cursor.fetchall()

        if(row[0][0] >= int(seats)):
            print("Connecting to payment gateway...")
            print("Payment Successful")
            k = abs(row[0][0] - int(seats))
            sql = "update flight set seatcount = %s where flightid = %s"
            cursor.execute(sql,(k, flightid))
            db.commit()
            cursor.close()
            db.close()
            return True
        else:
            #print("Seats not available for specified flights !")
            return False

