create database if not exists shapes_r_us;
use shapes_r_us;
CREATE TABLE IF NOT EXISTS CUSTOMER (
  Cust_email varchar(255) PRIMARY KEY NOT NULL,
  Cust_Lname varchar(255) Not Null,
  Cust_Fname varchar(255) Not Null,
  streetName varchar(255) Not Null,
  city varchar(255) Not Null,
  province varchar(255) Not Null,
  phoneNum varchar(10) Not Null);
CREATE TABLE IF NOT EXISTS EMPLOYEE (
  Emp_ID int AUTO_INCREMENT PRIMARY KEY NOT NULL,
  Emp_Lname varchar(255) Not Null,
  Emp_Fname varchar(255) Not Null,
  salary decimal(10, 2) Not Null,
  streetName varchar(255) Not Null,
  city varchar(255) Not Null,
  province varchar(255) Not Null,
  phoneNum varchar(10) Not Null);
CREATE TABLE IF NOT EXISTS VENDOR (
  vend_ID int AUTO_INCREMENT PRIMARY KEY Not Null,
  vendName varchar(255) Not Null,
  streetName varchar(255) Not Null,
  city varchar(255) Not Null,
  province varchar(255) Not Null,
  phoneNum varchar(10) Not Null);
CREATE TABLE IF NOT EXISTS PRODUCT (
  product_ID int AUTO_INCREMENT PRIMARY KEY Not Null,
  productName varchar(255),
  vend_ID int Not Null,
  productCost decimal(10,2) Not Null,
  inventory int Not Null,
  productDesc varchar(255),
  CONSTRAINT FOREIGN KEY (vend_ID) REFERENCES VENDOR (vend_ID));
CREATE TABLE IF NOT EXISTS INVOICE (
  Invoice_ID int AUTO_INCREMENT PRIMARY KEY NOT NULL,
  Emp_ID int Not Null,
  Cust_email varchar(255) Not Null,
  timeSold datetime Not Null,
  CONSTRAINT FOREIGN KEY (Emp_ID) REFERENCES EMPLOYEE (Emp_ID),
  CONSTRAINT FOREIGN KEY (Cust_email) REFERENCES CUSTOMER (Cust_email));
CREATE TABLE IF NOT EXISTS LINE_ITEM (
  Line_ID int AUTO_INCREMENT PRIMARY KEY NOT NULL,
  product_ID int Not Null,
  vend_ID int Not Null,
  Invoice_ID int Not Null,
  quantitySold int Not Null,
  CONSTRAINT FOREIGN KEY (product_ID) REFERENCES PRODUCT (product_ID),
  CONSTRAINT FOREIGN KEY (vend_ID) REFERENCES PRODUCT (vend_ID),
  CONSTRAINT FOREIGN KEY (Invoice_ID) REFERENCES INVOICE (Invoice_ID));
INSERT INTO CUSTOMER(Cust_email, Cust_Lname, Cust_Fname, streetName, city, province, phoneNum) VALUES ("bob.lablaw@freemail.com", "Loblaw", "Bob", "My Mom's Basement", "St. John's", "NL", "7095551234");
INSERT INTO EMPLOYEE(Emp_ID, Emp_Lname, Emp_Fname, salary, streetName, city, province, phoneNum) VALUES (23, "Burgandy", "Ron", 80000.00, "123 Main Street", "St. John's", "NL", "7091116789");
INSERT INTO VENDOR(vend_ID, vendName, streetName, city, province, phoneNum) VALUES (1, "Octo-Gone", "8 Eighty Street", "St. John's", "NL", "7098888888");
INSERT INTO PRODUCT(product_ID, productName, vend_ID, productCost, inventory, productDesc) VALUES (1, "Octagon", 1, 8.88, 8, "It's got 8 sides of fun and joy for you and your kids.");
INSERT INTO INVOICE(Invoice_ID, Emp_ID, Cust_email, timeSold) VALUES (42, 23, "bob.lablaw@freemail.com", '2021-03-30 09:52:33');
INSERT INTO LINE_ITEM(Line_ID, product_ID, vend_ID, Invoice_ID, quantitySold) VALUES (6, 1, 1, 42, 3);
INSERT INTO CUSTOMER(Cust_email, Cust_Lname, Cust_Fname, streetName, city, province, phoneNum) VALUES ('sal.manilla@freemail.com', 'Manilla', 'Sal', '1 Road Street', 'Cityville', 'AB', '7095551234');
INSERT INTO EMPLOYEE(Emp_ID, Emp_Lname, Emp_Fname, salary, streetName, city, province, phoneNum) VALUES (69, 'Smith', 'Charlotte', 420420, '2 Long Street', 'St. John\'s', 'NL', '7095555678');
INSERT INTO VENDOR(vend_ID, vendName, streetName, city, province, phoneNum) VALUES (2, 'Hyperbolia', '-i Pole Lane', 'Desitter', 'BC', '709555iiii');
INSERT INTO PRODUCT(product_ID, productName, vend_ID, productCost, inventory, productDesc) VALUES (2, 'Apeirogon', 2, 10.00, 1, 'A uniform polygon in hyperbolic space with an infinite number sides.');
INSERT INTO INVOICE (Invoice_ID, Emp_ID, Cust_email, timeSold) VALUES (13, 69, 'sal.manilla@freemail.com', '2021-03-30 09:47:42');
INSERT INTO LINE_ITEM(Line_ID, product_ID, vend_ID, Invoice_ID, quantitySold) VALUES (9, 2, 2, 13, 1);
INSERT INTO CUSTOMER ( Cust_email, Cust_Lname, Cust_Fname, streetName,city,province,phoneNum) values ('email@outlook.com', 'Joe', 'Joseph', '999 Real Street', 'Ottawa', 'ON', '7094589999');
INSERT INTO EMPLOYEE ( Emp_ID, Emp_Lname, Emp_Fname, salary,streetName,city,province,phoneNum) values (709, 'Bon', 'John', 40000, '234 Real location', 'Toronto', 'ON', '7097657654');
INSERT INTO VENDOR(vend_ID, vendName, streetName, city, province, phoneNum) values (3, 'The SquareHouse', '25 square place', 'Vancouver', 'BC', '7091234567');
INSERT INTO PRODUCT(product_ID, productName, vend_ID, productCost, inventory, productDesc) values (3, 'quantum square', 3, 22.50, 500, 'beyond your mortal comprehension');
INSERT INTO INVOICE ( Invoice_ID, Emp_ID,Cust_email,timeSold) values (907, 709, 'email@outlook.com', '2021-03-29 05:57:13');
INSERT INTO LINE_ITEM(Line_ID, product_ID, vend_ID, Invoice_ID, quantitySold) values ('123', 3, 3, 907, 490);
INSERT INTO CUSTOMER(Cust_email, Cust_Lname, Cust_Fname, streetName, city, province, phoneNum) VALUES ('billy.1@gmail.com', 'Bob', 'Billy', '123 Sea Road', 'St.Johns', 'NL', '7098731234');
INSERT INTO EMPLOYEE(Emp_ID, Emp_Lname, Emp_Fname, salary, streetName, city, province, phoneNum) VALUES (578, 'Jim', 'Gill', 10000, '34 Happy Lane', "St. John's", 'NL', '7096572356');
INSERT INTO VENDOR(vend_ID, vendName, streetName, city, province, phoneNum) VALUES (4, 'Jim', '67 Apples Road', 'St Johns', 'NL', '7096792356');
INSERT INTO PRODUCT(product_ID, productName, vend_ID, productCost, inventory, productDesc) VALUES (4, 'Triangle', 4, 15, 12, 'Shape with three sides');
INSERT INTO INVOICE(Invoice_ID, Emp_ID, Cust_email, timeSold) Values (2010, 578, 'billy.1@gmail.com', '2021-03-30 10:34:21');
INSERT INTO LINE_ITEM(Line_ID, product_ID, vend_ID, Invoice_ID, quantitySold) VALUES( 12, 4, 4, 2010, 12);

