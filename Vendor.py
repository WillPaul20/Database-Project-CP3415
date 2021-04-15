import mysql.connector
from secret_data import PASSWORD, USER_NAME, HOSTNAME

class Vendor:
    def __init__(self, user_name, password, hostname):
        self.user_name = user_name
        self.password = password
        self.hostname = hostname
        self.database_name = 'shapes_r_us'
        self.table_name = 'Vendor'

    def addVendor(self, vend_ID:int, vendName:str, streetName:str, city:str, province:str, phoneNum:str):
        assert type(vend_ID) == int and vend_ID > 0, "Vendor ID must be a non-negative int."
        assert type(vendName) == str, "vendName must be a string."
        assert type(streetName) == str, "vendName must be a string."
        assert type(city) == str, "vendName must be a string."
        assert type(province) == str, "vendName must be a string."
        assert type(phoneNum) == str, "vendName must be a string."
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                sql_script = f"INSERT into {self.table_name} (vend_ID, vendName, streetName, city, province, phoneNum) VALUES (%s, %s, %s, %s, %s, %s);"
                val = (vend_ID, vendName, streetName, city, province, phoneNum)
                mysql_cursor.execute(sql_script, val)
                mysql_connection.commit()
                print(mysql_cursor.rowcount, "record(s) affected.")
                
    def getAllVendors(self):
        # This function will print a list of products and information to the console
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT * FROM {self.table_name};")
                # Get the data from the database
                vendors = []
                for vendor in mysql_cursor:
                    vendors.append(str(vendor[0]).ljust(5) + vendor[1].ljust(20) + f"{vendor[2]} {vendor[3]}, {vendor[4]}".ljust(40) + vendor[5].ljust(10))
                return vendors
            
            
            
if __name__ == "__main__":
    v = Vendor(USER_NAME, PASSWORD, HOSTNAME)
    try:
        v.addVendor(6, "Penta", "5 Fifty Street", "St. John's", "NL", "7095555555")
    except Exception as ex:
        print(ex, "ERROR")
    print()
    
    for item in v.getAllVendors():
        print(item)