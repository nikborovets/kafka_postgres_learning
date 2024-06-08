import psycopg2

conn = psycopg2.connect(
    dbname='orders_db',
    user='user',
    password='password',
    host='localhost',
    port=5433
)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*), SUM(amount) FROM orders")
count, total_amount = cursor.fetchone()
print(f"Total Orders: {count}, Total Amount: {total_amount}")
