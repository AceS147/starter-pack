import mysql.connector

#pip install mysql-connector-python



config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_sql_password',
    'database': 'test_hand'
}

try:
    conn = mysql.connector.connect(**config)
    print ("✅ Connected to MySQL!")
except mysql.connector.Error as err:
    print("❌ MySQL error:", err)
