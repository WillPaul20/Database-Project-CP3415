import mysql.connector
from secret_data import PASSWORD, USER_NAME, HOSTNAME

class Employee:

    def __init__(self, user_name, password, hostname):
        self.user_name = user_name
        self.password = password
        self.hostname = hostname
        self.database_name = 'shapes_r_us'
        self.table_name = 'Employee'
    
    def login(self, id):
        # creates a list of employee IDs from the database, returns true if the id passed in is valid
        valid_ids = []
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f'USE {self.database_name}')
                mysql_cursor.execute(f'SELECT Emp_ID FROM {self.table_name}')
                
                for x in mysql_cursor:
                    valid_ids.append(x[0])
                        
                return (id in valid_ids)

    def addNewEmployee(self, emp_ID:int, empLname:str, empFname:str, salary:float, streetName:str, city:str, province:str, phoneNum:str):
        # Connect to the database using the connectors
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                sql = f"INSERT INTO {self.table_name} (emp_id, Emp_Lname, Emp_Fname, salary, streetName, city, province, phoneNum) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                vals = (emp_ID, empLname, empFname, salary, streetName, city, province, phoneNum)
                mysql_cursor.execute(sql, vals)
                mysql_connection.commit()
                
    
    def getEmployeeInfo(self, emp_id:int):
        assert type(emp_id) == int, "emp_id is required to be an int."
        # Connect to the database using the connectors
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                # Get the data from the database
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM {self.table_name} WHERE emp_ID = {emp_id}")
                print("-"*85)
                print("ID".ljust(5), "Employee Name".ljust(20), "Salary".ljust(15), "Address".ljust(30), "Phone".ljust(10))
                print("-"*85)
                for emp in mysql_cursor:
                    print(str(emp[0]).ljust(5), f"{emp[2]} {emp[1]}".ljust(20), f"${emp[3]}".ljust(15), f"{emp[4]} {emp[5]}, {emp[6]}".ljust(30), emp[7].ljust(10))
                print("-"*85)
                
               
    def getAllEmployees(self):
        # Connect to the database using the connectors
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM {self.table_name}")
                # Get the data from the database
                print("-"*95)
                print("ID".center(5), "Employee Name".center(25), "Salary".center(10), "Address".center(40), "Phone".center(10))
                print("-"*95)
                for emp in mysql_cursor:
                    print(str(emp[0]).center(5), f"{emp[2]} {emp[1]}".center(25), str(emp[3]).center(10), f"{emp[4]} {emp[5]}, {emp[6]}".center(40), emp[7].center(10))
                print("-"*95)

    
if __name__ == '__main__':
    e = Employee(USER_NAME, PASSWORD, HOSTNAME)
    print(e.login(69))
    print(e.login(11))
    e.getEmployeeInfo(69)
    e.getEmployeeInfo(11)
    
    try:
        e.addNewEmployee(1, "Python", "Monty", 120921.35, "22 Jump Street", "Victoria", "BC", "5551234567")
        e.getEmployeeInfo(710)
        e.getEmployeeInfo(1)
        e.addNewEmployee(710, "Friedman", "Max", 21876.99, "21 Jump Street", "Victoria", "BC", "5551239876")
    except Exception as ex:
        print(ex, "ERROR")
        
    print()
    e.getAllEmployees()
