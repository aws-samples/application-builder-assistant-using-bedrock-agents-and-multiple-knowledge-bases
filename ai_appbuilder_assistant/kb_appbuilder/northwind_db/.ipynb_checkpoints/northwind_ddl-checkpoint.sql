-- <EXAMPLES>
-- Few Examples of SQLite sql queries that can answer questions from Northwind database are:

-- Question: Get subtotal for each order.
-- Query
select OrderID, 
    format(sum(UnitPrice * Quantity * (1 - Discount)), 2) as Subtotal
from [Order Details]
group by OrderID
order by OrderID;

--Question: For each employee, get their sales amount, broken down by country name.
-- Query
select distinct b.*, a.CategoryName
from Categories a 
inner join Products b on a.CategoryID = b.CategoryID
where b.Discontinued = 0
order by b.ProductName;

-- Question: Sales amount for each quarter excluding discounts
-- Query
SELECT
  strftime('%Y', [OrderDate]) AS [Year],
  CASE
    WHEN CAST(strftime('%m', [OrderDate]) AS INTEGER) IN (1, 2, 3) THEN 'Q1'
    WHEN CAST(strftime('%m', [OrderDate]) AS INTEGER) IN (4, 5, 6) THEN 'Q2'
    WHEN CAST(strftime('%m', [OrderDate]) AS INTEGER) IN (7, 8, 9) THEN 'Q3'
    WHEN CAST(strftime('%m', [OrderDate]) AS INTEGER) IN (10, 11, 12) THEN 'Q4'
  END AS [Quarter],
  SUM([Quantity] * [UnitPrice] * (1 - [Discount])) AS [SalesAmount]
FROM [Order Details]
JOIN [Orders] ON [Order Details].[OrderID] = [Orders].[OrderID]
GROUP BY [Year], [Quarter]
ORDER BY [Year], [Quarter];


---
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;



SET default_tablespace = '';

SET default_with_oids = false;


---
--- drop tables
---


DROP TABLE IF EXISTS CustomerCustomerDemo;
DROP TABLE IF EXISTS CustomerDemographics;
DROP TABLE IF EXISTS employee_territories;
DROP TABLE IF EXISTS [Order Details];
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS shippers;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS territories;
DROP TABLE IF EXISTS us_states;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS employees;

-- <SCHEMA>
-- Database schema: Below are the Tables and Columns to be used for answering user questions 
-- Name: categories; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE categories (
    category_id smallint NOT NULL PRIMARY KEY,
    category_name character varying(15) NOT NULL,
    description text,
    picture bytea
);


--
-- Name: CustomerDemographics; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE CustomerDemographics (
    customer_type_id bpchar NOT NULL PRIMARY KEY,
    customer_desc text
);


--
-- Name: customers; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE customers (
    customer_id bpchar NOT NULL PRIMARY KEY,
    company_name character varying(40) NOT NULL,
    contact_name character varying(30),
    contact_title character varying(30),
    address character varying(60),
    city character varying(15),
    region character varying(15),
    postal_code character varying(10),
    country character varying(15),
    phone character varying(24),
    fax character varying(24)
);

--
-- Name: CustomerCustomerDemo; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE CustomerCustomerDemo (
    customer_id bpchar NOT NULL,
    customer_type_id bpchar NOT NULL,
    PRIMARY KEY (customer_id, customer_type_id),
    FOREIGN KEY (customer_type_id) REFERENCES customer_demographics,
    FOREIGN KEY (customer_id) REFERENCES customers
);

--
-- Name: employees; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE employees (
    employee_id smallint NOT NULL PRIMARY KEY,
    last_name character varying(20) NOT NULL,
    first_name character varying(10) NOT NULL,
    title character varying(30),
    title_of_courtesy character varying(25),
    birth_date date,
    hire_date date,
    address character varying(60),
    city character varying(15),
    region character varying(15),
    postal_code character varying(10),
    country character varying(15),
    home_phone character varying(24),
    extension character varying(4),
    photo bytea,
    notes text,
    reports_to smallint,
    photo_path character varying(255),
	FOREIGN KEY (reports_to) REFERENCES employees
);


--
-- Name: suppliers; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE suppliers (
    supplier_id smallint NOT NULL PRIMARY KEY,
    company_name character varying(40) NOT NULL,
    contact_name character varying(30),
    contact_title character varying(30),
    address character varying(60),
    city character varying(15),
    region character varying(15),
    postal_code character varying(10),
    country character varying(15),
    phone character varying(24),
    fax character varying(24),
    homepage text
);


--
-- Name: products; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE products (
    product_id smallint NOT NULL PRIMARY KEY,
    product_name character varying(40) NOT NULL,
    supplier_id smallint,
    category_id smallint,
    quantity_per_unit character varying(20),
    unit_price real,
    units_in_stock smallint,
    units_on_order smallint,
    reorder_level smallint,
    discontinued integer NOT NULL,
	FOREIGN KEY (category_id) REFERENCES categories,
	FOREIGN KEY (supplier_id) REFERENCES suppliers
);


--
-- Name: region; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE region (
    region_id smallint NOT NULL PRIMARY KEY,
    region_description bpchar NOT NULL
);


--
-- Name: shippers; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE shippers (
    shipper_id smallint NOT NULL PRIMARY KEY,
    company_name character varying(40) NOT NULL,
    phone character varying(24)
);


--
-- Name: orders; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE orders (
    order_id smallint NOT NULL PRIMARY KEY,
    customer_id bpchar,
    employee_id smallint,
    order_date date,
    required_date date,
    shipped_date date,
    ship_via smallint,
    freight real,
    ship_name character varying(40),
    ship_address character varying(60),
    ship_city character varying(15),
    ship_region character varying(15),
    ship_postal_code character varying(10),
    ship_country character varying(15),
    FOREIGN KEY (customer_id) REFERENCES customers,
    FOREIGN KEY (employee_id) REFERENCES employees,
    FOREIGN KEY (ship_via) REFERENCES shippers
);


--
-- Name: territories; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE territories (
    territory_id character varying(20) NOT NULL PRIMARY KEY,
    territory_description bpchar NOT NULL,
    region_id smallint NOT NULL,
	FOREIGN KEY (region_id) REFERENCES region
);


--
-- Name: employee_territories; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE employee_territories (
    employee_id smallint NOT NULL,
    territory_id character varying(20) NOT NULL,
    PRIMARY KEY (employee_id, territory_id),
    FOREIGN KEY (territory_id) REFERENCES territories,
    FOREIGN KEY (employee_id) REFERENCES employees
);


--
-- Name: Order Details; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE [Order Details] (
    order_id smallint NOT NULL,
    product_id smallint NOT NULL,
    unit_price real NOT NULL,
    quantity smallint NOT NULL,
    discount real NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products,
    FOREIGN KEY (order_id) REFERENCES orders
);


--
-- Name: us_states; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE us_states (
    state_id smallint NOT NULL PRIMARY KEY,
    state_name character varying(100),
    state_abbr character varying(2),
    state_region character varying(50)
);
