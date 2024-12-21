--Tables

CREATE TABLE Customer (
    customer_id int PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    password char(16) NOT NULL,
    address VARCHAR(255),
    mail_address VARCHAR(100),
    phone_number VARCHAR(30)
);

CREATE TABLE Order_ (
    order_id INT PRIMARY KEY,
    order_time TIMESTAMP NOT NULL,
    customer_id INT NOT NULL REFERENCES Customer(customer_id)
);

CREATE TABLE Category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE Product (
    product_id INT PRIMARY KEY,
    product_description VARCHAR(255),
    product_amount INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category_id INT REFERENCES Category(category_id),

    CONSTRAINT chk_amount CHECK (product_amount >= 0),
    CONSTRAINT chk_price CHECK (price >= 0)
);

CREATE TABLE Seller (
    seller_ssn VARCHAR(15) PRIMARY KEY,
    seller_name VARCHAR(100) NOT NULL,
    password char(16) NOT NULL,    
    address VARCHAR(255),
    mail_address VARCHAR(100),
    phone_number VARCHAR(30)
);

-- Relationships
-- includes table
CREATE TABLE Order_Product (
    order_id INT REFERENCES Order_(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES Product(product_id),
	order_amount INT NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

-- self referencing to create subcategories
ALTER TABLE Category
ADD COLUMN parent_category_id INT REFERENCES Category(category_id);

CREATE TABLE Review (
    customer_id INT REFERENCES Customer(customer_id),
    product_id INT REFERENCES Product(product_id),
    review_body TEXT,
    review_rating INT CHECK (review_rating BETWEEN 1 AND 5),
    PRIMARY KEY (customer_id, product_id)
);

CREATE TABLE Product_Seller (
    product_id INT REFERENCES Product(product_id),
    seller_ssn VARCHAR(15) REFERENCES Seller(seller_ssn),
    PRIMARY KEY (product_id, seller_ssn)
);

-- views, sequences

-- kategorisi olan tüm ürünleri listeler
CREATE VIEW Category_products_view AS
SELECT 
    product_id, 
    product_description, 
    price, 
    category_name
FROM Product
JOIN Category 
ON Product.category_id = Category.category_id;

-- sequence for customer_id (customer table)
CREATE SEQUENCE customer_sequence
MINVALUE 11
INCREMENT BY 1;

-- sequence for order_id (order_ table)
CREATE SEQUENCE order_sequence
MINVALUE 1000
INCREMENT BY 1;

