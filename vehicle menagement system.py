import sqlite3
import sys
from datetime import datetime
from tabulate import tabulate


class inventory:

    @classmethod
    def available_cars(cls, mail):
        data = ''

        data = input(
            "You can search cars options below:\n\t1.ALL CARS: \n\t2.ADD cars: \n\t3.Update record: \n\t4.Delete "
            "record: \nEnter:")
        if data == "1":
            cls.show_data()
        elif data == "2":
            cls.add_data(mail)
        elif data == "3":
            cls.update_price()
        elif data == "4":
            cls.del_data()
        else:
            print("Wrong input only integers value can be inserted from 1 to 4")
            cls.available_cars(mail)

    @classmethod
    def add_data(cls, mail):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cars (car_id INTEGER PRIMARY KEY, name TEXT NOT NULL,make TEXT,
        model TEXT,variant TEXT,cc TEXT, engine_type TEXT,registration_city TEXT,registration TEXT,price TEXT,
        purchasing_date TEXT, selling_date TEXT,purchasing_price FLOAT,selling_price FLOAT,profit_loss FLOAT)''')

        car_id = True
        while car_id:
            car_id = int(input("Enter the car_id: "))
            if inventory.chk_data(car_id):
                print("CAR ID already exists. Try with another id\n")
                cls.add_data(mail)
            else:
                pass
            name = input("Enter a name of the car : ")
            make = input("Enter make of the car: ")
            model = input("Enter model of the car: ")
            variant = input("Enter variant of the car : ")
            cc = input("Enter the cc of the car: ")
            engine_type = input("Enter the engine_type of the car: ")
            registration_city = input("Enter the registration city of the car: ")
            registration = input("Enter the registration number of the car : ")
            price = input("Enter the price: ")
            purchasing_date = input("Enter the purchasing date of the car: ")
            selling_date = input("Enter the selling date of the car: ")
            purchasing_price = float(input("Enter the purchasing price of the car:"))
            selling_price = float(input("Enter the selling price of the car: "))
            profit_loss = float(selling_price) - float(purchasing_price)
            if selling_price > purchasing_price:
                print("profit", profit_loss)
            elif purchasing_price > selling_price:
                print("loss", profit_loss)
            else:
                print("no profit no loss")
                break
            cursor.execute("INSERT INTO cars (car_id, name,make,model,variant,cc,engine_type,"
                           "registration_city,registration,price,purchasing_date,selling_date,purchasing_price,"
                           "selling_price,profit_loss) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (car_id, name, make, model, variant, cc, engine_type, registration_city, registration,
                            price, purchasing_date, selling_date, purchasing_price, selling_price, profit_loss))
            conn.commit()
            conn.close()
            want = input("\nDo you want to add more cars Y/N ? ")
            if want == "y" or want == "Y":
                cls.add_data(mail)
            else:
                print("ThankYOU")
                break

    @classmethod
    def show_data(cls):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars")
        cars = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        print(tabulate(cars, headers=column_names, tablefmt='fancy_grid', colalign=("left",)))
        conn.close()

    @classmethod
    def show_data_buyer(cls):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name,make, model,variant,cc,engine_type,registration_city,registration, price FROM cars")
        cars = cursor.fetchall()
        column_names = ['name', 'make', 'model', 'variant', 'cc', 'engine_type', 'registration_city', 'registration',
                        'price']
        print(tabulate(cars, headers=column_names, tablefmt='fancy_grid', colalign=("left",)))
        conn.close()

    @classmethod
    def search_by_name(cls):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        name = input("Enter name of the car:")
        query = cursor.execute(
            "SELECT name, make, model, variant, cc, engine_type, registration_city, registration, price FROM cars "
            "WHERE name=?",
            (name,))
        car = cursor.fetchone()

        column_names = ['name', 'make', 'model', 'variant', 'cc', 'engine_type', 'registration_city', 'registration',
                        'price']
        if car:
            print(tabulate([car], headers=column_names, tablefmt='fancy_grid', colalign=("left",)))
        else:
            print("No cars found with this name '{}'".format(name))
        conn.close()
        if inventory.chk_data(name):
            pass
        else:
            cls.search_by_name()

    @classmethod
    def search_by_registration_city(cls):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        registration_city = input("Enter registration_city of the car:")
        cursor.execute(
            "SELECT name, make, model, variant, cc, engine_type, registration_city, registration, price FROM cars "
            "WHERE registration_city=?",
            (registration_city,))
        cars = cursor.fetchall()

        column_names = ['name', 'make', 'model', 'variant', 'cc', 'engine_type', 'registration_city', 'registration',
                        'price']
        if cars:
            print(tabulate(cars, headers=column_names, tablefmt='fancy_grid', colalign=("left",)))
        else:
            print("No cars found with registration city '{}'".format(registration_city))

        conn.close()
        if inventory.chk_data(registration_city):
            pass
        else:
            cls.search_by_registration_city()

    @classmethod
    def del_data(cls):
        cls.show_data()
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        query = "DELETE FROM cars WHERE car_id =?"
        car_id = input("Enter the CAR ID to delete record: ")
        if inventory.chk_data(car_id):
            pass
        else:
            print("NO record found")
            cls.del_data()
        cursor.execute(query, (car_id,))
        conn.commit()
        conn.close()

    @classmethod
    def update_price(cls):
        cls.show_data()
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        query = "UPDATE cars SET price=? WHERE car_id=?"
        car_id = input("Enter Car Id :")
        if inventory.chk_data(car_id):
            u = input("Enter new updated price: ")
            cursor.execute(query, (u, car_id))
        else:
            print("CAR ID not found")
            cls.update_price()
        conn.commit()
        cls.show_data()
        conn.close()

    @classmethod
    def chk_data(cls, car_id):
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM cars WHERE car_id=?", (car_id,))
        result = c.fetchone()
        conn.close()
        if result is None:
            return False
        else:
            return True

class Buyer(inventory):
    def __init__(self, name):
        self.name = name

    @classmethod
    def buy(cls, mail):
        user_input = ''
        user_input = int(input("-----------Welcome to ELITE MOTORS------------ \n"
                               "Are you a buyer or a owner? \n\t"
                               "1. Buyer\n\t"
                               "2. Owner\n\t"
                               "Please enter:  "))
        if user_input == 1:
            return Customer.choice(mail)
        elif user_input == 2:
            return Buyer.owner(mail)
        else:
            print("error")
            cls.buy(mail)

    @classmethod
    def owner(cls, mail):
        print("Welcome owner!")
        inventory.available_cars(mail)


class Customer(inventory):
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

    @classmethod
    def choice(cls, mail):
        while True:
            data1 = ''
            data1 = input("We have the following cars\n\t1.ALL CARS\n\t2.Search by name\n\t3.Search by "
                          "registration_city\n\t4.MainMenu\n\tENTER:")
            if data1 == "1":
                return inventory.show_data_buyer()
            elif data1 == "2":
                return inventory.search_by_name()
            elif data1 == "3":
                return inventory.search_by_registration_city()
            elif data1 == "4":
                Buyer.buy(mail)
            else:
                print("Only integers values can be inserted from 1 to 4")
                cls.choice(mail)
                break

    @classmethod
    def sell_car(cls, mail):
        car_id = input("Enter the Car Id:")
        if inventory.chk_data(car_id):
            pass
        else:
            cls.sell_car(mail)

    @classmethod
    def chk_quantity(cls, car_id, customer_req, mail):
        conn = sqlite3.connect('Store.db')
        cur = conn.cursor()
        customer_req = input("Enter the car name: ")
        cur.execute("SELECT name FROM cars WHERE car_id=?", (car_id,))
        result = cur.fetchone()

        if result is None:
            return "Car not found."
        car_name = result[1]
        if car_name == customer_req:
            print("\nCar is available: {}".format(car_name))
            print("Please Enter that is available......!\n")
            return False
        else:
            cls.remove_data(customer_req, car_id, mail)
    @classmethod
    def remove_data(cls, car_id, customer_req, mail):
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        print(mail)
        cur.execute("UPDATE cars SET name=? WHERE car_id = ?", (customer_req, car_id))
        cur.execute("SELECT price FROM cars WHERE car_id=?", (car_id,))
        num = cur.fetchone()
        one = num[1]
        print(one)
        total_price = one * customer_req
        print(total_price)
        cur.execute("SELECT car_id,name FROM cars WHERE car_id=?", (car_id,))
        data2 = cur.fetchone()
        car_id = data2[0]
        print(car_id)
        name = data2[1]
        print(name)
        print(data2)
        cur.execute("SELECT user_id,user_email FROM users WHERE user_email=?", (mail,))
        data3 = cur.fetchone()
        user_id = data3[0]
        print(user_id)
        user_email = data3[1]
        print(user_email)
        print(data3)
        car_details = customer_req
        date_time = datetime.now()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS sales (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        car_id TEXT,
                        name TEXT,
                        user_id TEXT,
                        user_email TEXT,
                        car_details TEXT,
                        total_price TEXT,
                        date_time TIMESTAMP
                        )''')
        cur.execute("INSERT INTO sales(car_id,name,user_id,user_email,car_details,total_price,date_time)VALUES(?,?,?,"
                    "?,?,?,?)", (car_id, name, user_id, user_email, car_details, total_price, date_time))
        conn.commit()
        cls.show_data()
        conn.close()
class User:
    @classmethod
    def user_type(cls):
        import sqlite3
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_role TEXT NOT NULL,
                        user_email TEXT NOT NULL,
                        time_date TIMESTAMP)''')
        user_email = input("Enter your email address: ")
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_email=?", (user_email,))
        result = cursor.fetchone()
        if result is None:
            return cls.add_user(user_email)
        mail = result[2]
        if result:
            user_role = result[1]
            if user_role == "customer":
                print("Customer")
                return Customer.choice(mail)
            elif user_role == "owner":
                return Buyer.owner(mail)
        else:

            print("Email not found.........!\nMention your role to add your email: ")
            user_role = input("Enter your Type (customer/owner): ")
            if user_role.lower() == "customer":
                cursor.execute("INSERT INTO users (user_email, user_role) VALUES (?, ?)", (user_email, "customer"))
                print("New Customer has been added....!")
            elif user_role.lower() == "owner":
                cursor.execute("INSERT INTO users (user_email, user_role) VALUES (?, ?)", (user_email, "owner"))
                print("New Owner has been added.......!")
            else:
                print("Invalid role.")
        conn.commit()
        conn.close()
    @classmethod
    def add_user(cls, user_email):
        time_date = datetime.now()
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        print("Email not found\n Mention your role to add your email:")
        user_role = input("Enter your type\n--customer\n--owner\nEnter:")
        if user_role.lower() == "customer":
            cursor.execute("INSERT INTO users (user_email, user_role, time_date) VALUES (?, ?, ?)",
                           (user_email, "customer", time_date))
            print("New Customer has been added....!")
        elif user_role.lower() == "owner":
            cursor.execute("INSERT INTO users (user_email, user_role, time_date) VALUES (?, ?, ?)",
                           (user_email, "owner", time_date))
            print("New Owner has been added.......!")
        else:
            print("Invalid role.")
        conn.commit()
        conn.close()

def main():
    user = User()
    user.user_type()

main()