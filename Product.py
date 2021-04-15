import mysql.connector
from secret_data import PASSWORD, USER_NAME, HOSTNAME

class Product:
    def __init__(self, user_name, password, hostname):
        self.user_name = user_name
        self.password = password
        self.hostname = hostname
        self.database_name = 'shapes_r_us'
        self.table_name = 'Product'
        
    def getAllProducts(self):
        # returns a list of formatted strings which represent product data
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT product_ID, productName, vendName, productCost, inventory FROM {self.table_name} INNER JOIN vendor ON product.vend_ID = vendor.vend_ID ORDER BY product_ID;")
                products = []
                for product in mysql_cursor:
                    products.append(str(product[0]).ljust(5) + product[1].ljust(20) + product[2].ljust(20) + f"${product[3]}".ljust(10) + str(product[4]).ljust(10))
                return products
    
    def getProductByID(self, product_ID):
        # returns a tuple representing a single product given an ID
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT product_ID, productName, vendName, productCost, inventory FROM {self.table_name} INNER JOIN vendor ON product.vend_ID = vendor.vend_ID WHERE product_ID = {product_ID}")
                for product in mysql_cursor:
                    return product
                
    def getZeroStock(self):
        # returns a list of formatted strings which represent products whose inventory count == 0
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT product_ID, productName, vendName, productCost, inventory FROM {self.table_name} INNER JOIN vendor ON product.vend_ID = vendor.vend_ID WHERE product.inventory = 0")
                zero_stock = []
                for product in mysql_cursor:
                    zero_stock.append(str(product[0]).ljust(5) + product[1].ljust(20) + product[2].ljust(20) + f"${product[3]}".ljust(10) + str(product[4]).ljust(10))
                return zero_stock
                
            
    def purchaseProduct(self, product_ID, quantity):
        # removes a given quantity of a product from the database
        assert type(product_ID) == int and product_ID > 0, "Product ID must be a non-negative integer."
        assert type(quantity) == int, "Quantity must be an integer."
        # check that there is enough product in stock
        with mysql.connector.connect(host=self.hostname, user=self.user_name, password=self.password) as mysql_connection:
            with mysql_connection.cursor() as mysql_cursor:
                mysql_cursor.execute(f"USE {self.database_name}")
                mysql_cursor.execute(f"SELECT product_ID, productName, vendName, productCost, inventory FROM {self.table_name} INNER JOIN vendor ON product.vend_ID = vendor.vend_ID WHERE product_ID = {product_ID}")
                contents = mysql_cursor.fetchall()
                # If not enough stock, print appropriate message to user. Otherwise, update inventory.
                if contents[0][4] < quantity:
                    print(f"There is not enough product ({contents[0][1]}) available for this request. Current stock: {contents[0][4]}")
                else:
                    mysql_cursor.execute(f"UPDATE {self.table_name} SET inventory = inventory - {quantity} WHERE product_ID = {product_ID}")
                    mysql_connection.commit()
                
                
if __name__ == '__main__':
    p = Product(USER_NAME, PASSWORD, HOSTNAME)
    print(p.getAllProducts())
    print(p.getProductByID(2))
    print(p.getZeroStock())
    p.purchaseProduct(3, 10)
    p.purchaseProduct(2, 1)
    print(p.getAllProducts())
    
    try:
        p.addProduct(5, "Rhombus", 3, 45.23, 30, "A square, that has been shoved and squat.")
    except Exception as ex:
        print(ex, "ERROR")
        
    p.getAllProducts()
    