import Employee, Product, Sale, Customer, Vendor, Invoice
from secret_data import PASSWORD, USER_NAME, HOSTNAME
import mysql.connector
import datetime

from mysql.connector import ProgrammingError

emp_connector = Employee.Employee(USER_NAME, PASSWORD, HOSTNAME)
prod_connector = Product.Product(USER_NAME, PASSWORD, HOSTNAME)
sale_handler = Sale.Sale(USER_NAME, PASSWORD, HOSTNAME)
cust_connector = Customer.Customer(USER_NAME, PASSWORD, HOSTNAME)
vend_connector = Vendor.Vendor(USER_NAME, PASSWORD, HOSTNAME)
invoice_connector = Invoice.Invoice(USER_NAME, PASSWORD, HOSTNAME)

def debug_reset():
    # added for debugging purposes to reset the database to master without having to open MySQL
    # can still be called by running the hidden command 'R' in the main menu
    
    # read the script and clean it up
    with open('reset.sql', 'r') as reset:
        commands = reset.read().split(';\n')
    # connect to mysql and execute 
    with mysql.connector.connect(host=HOSTNAME, user=USER_NAME, password=PASSWORD) as mysql_connection:
        with mysql_connection.cursor() as mysql_cursor:
            mysql_cursor.execute('drop database if exists shapes_r_us')
            for line in commands:
                mysql_cursor.execute(line.strip())
            mysql_connection.commit()

def login(id):
    # used to secure the program against non-Employees
    try:
        return emp_connector.login(int(id))
    except ValueError:
        print(ValueError, 'id must be an int')
        return False
    except ProgrammingError as pe:
        print(pe, 'database not found, please choose initialize\n exiting...')
        exit()
    
def main_menu():
    print('1. Add Customer')
    print('2. Generate Reports')
    print('3. Transaction')
    print('0. Exit')
    
def report_menu():
    while True:
        print('1. List All Products')
        print('2. List All Invoices')
        print('3. View detailed invoice')
        print('4. List products at zero stock')
        print('5. List active customers')
        print('0. Exit')
        
        command = input('\nSelect an option: ')
        if command in REPORT_MENU:
            REPORT_MENU[command]()
        elif command == '0':
            break
        else:
            print('Invalid command try again plz')


def addCustomer():
    # the function should return the customer email,
    # this saves the user energy if they have just created a new account
    
    # Get user input.
    custEmail = input("Enter customer email...")
    custFirstName = input("Enter customer First name...")
    custLastName = input("Enter customer Last name...")
    custStreetName = input("Enter customer street name/number...")
    custCity = input("Enter customer city...")
    custProvince = input("Enter customer province...")
    custPhone = input("Enter customer phone number...")
    # Pass information into the database to insert new customer.
    try:
        cust_connector.addNewCustomer(custEmail, custLastName, custFirstName, custStreetName, custCity, custProvince, custPhone)
    except TypeError as te:
        print(te, "Ensure data is entered in the correct format.\n Exiting...")
    except Exception as e:
        print(e, "ERROR.\n Exiting...")
        
    return custEmail
        
def transaction():
    global login_id 
    choice = input('New customer? [y] ')
    if choice == 'y':
        cust_key = addCustomer()
    else:
        cust_key = input('Enter customer email > ')
    
    if cust_connector.getCustomerInfo(cust_key):
        # taking advantage of the fact that this method only has a return on valid customer keys
        cart = []
        while True:
            # a new sub menu for the transaction
            print('1. View cart')
            print('2. Add product to cart')
            print('3. Remove item from cart')
            print('4. Purchase cart')
            print('0. Exit (cart will not be saved)')
            
            command = input('\nSelect an option: ')
            if command == '1':
                view_cart(cart)
            elif command == '2':
                listProducts()
                addProductToCart(cart)
            elif command == '3':
                view_cart(cart)
                cart = removeProductFromCart(cart)   
            elif command == '4':
                completeSale(login_id, cust_key, cart)
            elif command == '0':
                break
            else:
                print('Invalid command try again plz')
    else:
        print('Customer not found, please try again\nexiting... ')
    
def view_cart(cart):
    print('='*40)
    print('ID'.ljust(5), 'Product Name'.ljust(30), 'QTY'.ljust(5))
    print('='*40)
    for item in cart:
        print(item[0].ljust(5), prod_connector.getProductByID(item[0])[1].ljust(30), item[1].ljust(5))
    
def addProductToCart(cart):
    try:
        product_ID = input('Enter product ID > ')
        product = prod_connector.getProductByID(product_ID)
        if not product:
            print('Invalid product ID\nexiting...')
            return
        quantity = input('Quantity: ')
        if product[-1] < int(quantity):
            print('Stock is too low!\nexiting...')
            return
    except Exception as e:
        print(e, '\nexiting...')
    else:
        cart.append((product_ID, quantity))
    
def removeProductFromCart(cart):
    # after asking for input from the user, returns a new cart
    choice = input('Enter product ID to remove > ')
    new_cart = []
    for item in cart:
        if item[0] != choice:
            new_cart.append(item)
        if item[0] == choice:
            print('product removed from cart')
    if new_cart == cart:
        print('product not in cart')
    return new_cart
        
def completeSale(login_id, cust_id, cart):
    total = 0.00
    for item in cart:
        product = prod_connector.getProductByID(item[0])
        total += float(product[-2]) * int(item[1])
    emp_id = input(f'TOTAL PRICE = ${total}\nre-enter employee id to confirm > ')
    if emp_id != login_id:
        print('That is the incorrect employee id\nexiting... ')
        return
    # generateInvoice returns the ID, as it is generated based on system time
    invoice = sale_handler.generateInvoice(emp_id, cust_id)
    #pass this invoice id into the sale_handler to create our line_items
    sale_handler.createLineItems(cart, invoice)
    
    for item in cart:
        prod_connector.purchaseProduct(int(item[0]), int(item[1]))
    
def listProducts():
    print("-"*70)
    print("ID".ljust(5), "Product Name".ljust(20), "Vendor Name".ljust(15), "Unit Cost".ljust(10), "Inventory".ljust(10))
    print("-"*70)
    products = prod_connector.getAllProducts()
    for line in products:
        print(line)
    print("-"*70)

def listInvoices():
    invoices = invoice_connector.getAllInvoices()
    print("-"*70)
    print("ID".ljust(15), "EMP".ljust(7), "Customer".ljust(30), "Date".ljust(15))
    print("-"*70)
    
    for invoice in invoices:
        print( str(invoice[0]).ljust(15) + str(invoice[1]).ljust(7) + invoice[2].ljust(30) + invoice[3].strftime('%d-%m-%y %H:%M').ljust(15))

def displayInvoice():
    ID = input('Enter a invoice id: ')
    
    try:
        invoice = invoice_connector.getInvoiceByID(ID)
    except:
        print('invoice not found\nexiting...')
        
    else:
        print(f"SALE ID {invoice[0]} COMPLETED BY EMPLOYEE {invoice[1]}\nTO {invoice[2]} ON {invoice[3]}")
        items =  invoice_connector.getInvoiceLinesByID(ID) 
        print("-"*50)
        print("Product Name".ljust(25), "Cost/Unit".ljust(10), "QTY".ljust(5), "Cost".ljust(5))
        print("-"*50)
        total = 0.0
        for item in items:
            cost = float(item[1]) * item[2]
            print( item[0].ljust(25) + str(item[1]).ljust(10) + '  ' + str(item[2]).ljust(5) + '${:.2f}'.format(cost))
            total += cost
        print('='*50)
        print("TOTAL VALUE: ".ljust(42) + '${:.2f}'.format(total))
        print("-" * 50)

def listZeroStock():
    zero_stock = prod_connector.getZeroStock()
    if zero_stock:
        print("-"*70)
        print("ID".ljust(5), "Product Name".ljust(20), "Vendor Name".ljust(20), "Unit Cost".ljust(10), "Inventory".ljust(10))
        print("-"*70)
        for line in zero_stock:
            print(line)
        print("-"*70)
        
    else:
        print('Good news everyone! There are no products at zero stock!\n')

def listActiveCustomers():
    active_customers = invoice_connector.getActiveCustomers()
    print("The following customers have purchased items in the past month: ")
    for customer in active_customers:
        print(customer[0])
        
#used dictionaries to store functions to make the main() method far easier to read.        
MAIN_MENU = {
    'R': debug_reset,
    '1': addCustomer, 
    '2': report_menu,
    '3': transaction
    }

REPORT_MENU = {
    '1': listProducts,
    '2': listInvoices,
    '3': displayInvoice,
    '4': listZeroStock,
    '5': listActiveCustomers
    }

    
def main():
    
    while True:
        global login_id
        login_id = input('Enter employee ID to sign in... ')
        if login(login_id):
            break
        else:
            print('Not a valid employee!')
    
    while True:
        main_menu()
        command = input('\nSelect an option: ')
        if command in MAIN_MENU:
            MAIN_MENU[command]()
        elif command == '0':
            break
        else:
            print('Invalid command try again plz')

if __name__ == '__main__':
    main()
