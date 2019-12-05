import mysql.connector as mysql

class CarBookingSaga(object):

    def getCar(self, dst, date):

        db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor = db.cursor()
        sql = "select carName from carList where City = %s && Date = %s"
        cursor.execute(sql, (dst, date))
        row = cursor.fetchall()
        lst = [] 
        for i in row:
            lst.append(i[0])

        cursor.close()
        db.close()
        return lst

        

    def bookCar(self, carName, cars):

        db = mysql.connect(host="localhost", user = "root", passwd = "testtest", database = "mydb")
        cursor = db.cursor()
        sql = "select carCount from carList where carName = %s"
        cursor.execute(sql, (carName,))
        row = cursor.fetchall()

        if(row[0][0] >= int(cars)):
            print("Connecting to payment gateway...")
            print("Payment Successful")
            k = abs(row[0][0] - int(cars))
            sql = "update carList set carCount = %s where carName = %s"
            cursor.execute(sql,(k, carName))
            db.commit()
            cursor.close()
            db.close()
            return True

        else:
            return False

