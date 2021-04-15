import mysql.connector
from secret_data import PASSWORD, USER_NAME, HOSTNAME

class Customer:
    def __init__(self, user_name, password, hostname):
        self.user_name = user_name
        self.password = password
        self.hostname = hostname
        self.database_name = 'shapes_r_us'
        self.table_name = 'Customer'

    def addNewCustomer(self, custEmail:str, custLname:str, custFname:str, streetName:str, city:str, province:str, phoneNum:str):
        assert type(custEmail) == str, "custEmail must be a string."
        assert type(custLname) == str, "custLname must be a string."
        assert type(custFname) == str, "custFname must be a string."
        assert type(streetName) == str, "streetName must be a string."
        assert type(city) == str, "city must be a string."
        assert type(province) == str, "province must be a string."
        assert type(phoneNum) == str, "phoneNum must be a string."
        # Connect to the database using the connectors
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                sql = f"INSERT INTO {self.table_name} (Cust_email, Cust_Lname, Cust_Fname, streetName, city, province, phoneNum) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                vals = (custEmail, custLname, custFname, streetName, city, province, phoneNum)
                mysql_cursor.execute(sql, vals)
                mysql_connection.commit()


    def getCustomerInfo(self, custEmail:str):
        assert type(custEmail) == str, "custEmail is required to be a string."
        # Connect to the database using the connectors
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM {self.table_name} WHERE Cust_email = '{custEmail}'")
                # Get the data from the database
                customers = []
                for cust in mysql_cursor:
                    customers.append(str(cust[0]).ljust(25) + f"{cust[2]} {cust[1]}".ljust(30) + f"{cust[3]} {cust[4]}, {cust[5]}".ljust(40) + cust[6].ljust(10))
                return customers
                                     
                                     
    def modifyCustomer(self, custEmail:str):
        pass


if __name__ == "__main__":
    c = Customer(USER_NAME, PASSWORD, HOSTNAME)
    print(c.getCustomerInfo("bob.lablaw@freemail.com"))
    
    try:
        c.addNewCustomer("job.bobber@freemail.com", "Jobs", "Robert", "23 Left Side Street", "Clarenville", "NL", "7094660987")
        print(c.getCustomerInfo("job.bobber@freemail.com"))
    except Exception as e:
        print(e, "\nERROR Duplicate entry. Customer already exists in database.")