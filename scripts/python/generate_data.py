# scripts/python/generate_data.py
import psycopg2
from faker import Faker
import random

fake = Faker()

# Kết nối DB
conn = psycopg2.connect(
    dbname="restaurant", user="admin", 
    password="Password123!", host="localhost", port="5432"
)
cur = conn.cursor()

# 1. Insert Customers (Có data bẩn: NULL email, duplicate)
print("Generating customers...")
for _ in range(1000):
    name = fake.name()
    email = fake.email() if random.random() > 0.1 else None # 10% NULL email
    # Cố tình tạo duplicate email
    if random.random() < 0.05: 
        email = "duplicate_test@example.com"
    
    cur.execute("INSERT INTO customers (full_name, email) VALUES (%s, %s)", (name, email))

# 2. Insert Restaurants
print("Generating restaurants...")
for _ in range(50):
    cur.execute("INSERT INTO restaurants (name, city) VALUES (%s, %s)", 
                (fake.company(), fake.city()))

# 3. Insert Orders (Có data bẩn: Invalid amount)
print("Generating orders...")
for _ in range(5000):
    cust_id = random.randint(1, 1000)
    rest_id = random.randint(1, 50)
    # Cố tình tạo amount < 0 (Invalid value)
    amount = round(random.uniform(-50.0, 200.0), 2) 
    cur.execute("""
        INSERT INTO orders (customer_id, restaurant_id, total_amount) 
        VALUES (%s, %s, %s)
    """, (cust_id, rest_id, amount))

conn.commit()
cur.close()
conn.close()
print("Data generation completed!")