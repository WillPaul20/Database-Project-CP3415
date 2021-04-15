import mysql.connector
from secret_data import PASSWORD, USER_NAME, HOSTNAME

class Invoice:
    def __init__(self, user_name, password, hostname):
        self.user_name = user_name
        self.password = password
        self.hostname = hostname
        self.database_name = 'shapes_r_us'
        self.table_name = 'invoice'
        
    def getAllInvoices(self):
        # returns a list of tuples representing invoice data 
        all_invoices = []
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"Use {self.database_name}")
                mysql_cursor.execute(f'SELECT * FROM {self.table_name}')
                #Get data from database
                for invoice in mysql_cursor:
                    all_invoices.append(invoice)
                return all_invoices
    
    def getInvoiceByID(self, ID):
        # returns the fields of a specific invoice given an ID
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f'SELECT * FROM {self.table_name} WHERE Invoice_ID = {ID}' )
                for invoice in mysql_cursor:
                    return invoice
            
    def getInvoiceLinesByID(self, ID):
        # returns every line item associated with a given invoice on ID
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f'SELECT product.productName, product.productCost, line_item.quantitySold FROM line_item join product ON line_item.product_ID = product.product_ID WHERE Invoice_ID = {ID}' )
                items = []
                for item in mysql_cursor:
                    items.append(item)
                    
                return items
        
    def getActiveCustomers(self):
        # returns a list of emails of only those customers who have been included on an invoice in the past month
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute("SELECT Cust_Email FROM Invoice WHERE (DATEDIFF(timeSold, NOW()) > -30)")
                return [item for item in mysql_cursor]
            
            
if __name__ == '__main__':
    i = Invoice(USER_NAME, PASSWORD, HOSTNAME)
    i.getAllInvoices()
    ID = input('id: ')
    print(i.getInvoiceByID(ID))