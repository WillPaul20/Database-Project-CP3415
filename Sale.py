import mysql.connector
import Product
from secret_data import PASSWORD, USER_NAME, HOSTNAME
from datetime import datetime
prod_connector = Product.Product(USER_NAME, PASSWORD, HOSTNAME)


class Sale:
    def __init__(self, user_name, password, hostname):
        self.user_name = user_name
        self.password = password
        self.hostname = hostname
        self.database_name = 'shapes_r_us'
    
    def generateInvoice(self, emp_id, cust_id):
        timeSold = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        invoice_id = datetime.now().strftime("%j%f")
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                sql_script = f"INSERT into invoice (Invoice_ID, Emp_ID, Cust_email, timeSold) VALUES ('{invoice_id}', '{emp_id}', '{cust_id}', '{timeSold}');"
                mysql_cursor.execute(sql_script)
                mysql_connection.commit()
        return invoice_id
      
    def createLineItems(self, cart, invoice_id):
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                for item in cart:
                    product_ID = item[0]
                    vend_ID = 1 # help
                    quantity_sold = item[1]
                    sql_script = f"INSERT into line_item (product_ID, vend_ID, Invoice_ID, quantitySold) VALUES ('{product_ID}', '{vend_ID}', '{invoice_id}', '{quantity_sold}');"
                    mysql_cursor.execute(sql_script)
                mysql_connection.commit()

if __name__ == '__main__':
    s = Sale(USER_NAME, PASSWORD, HOSTNAME)
    
    invoice_id = s.generateInvoice('69', 'sal.manilla@freemail.com')
    cart = [ ('1','1'), ('2','1'), ('4','1')]
    s.createLineItems(cart, invoice_id)