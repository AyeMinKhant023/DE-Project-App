import mysql.connector

# YOUR DATABASE INFO
db_config = {
    'user': 'admin',
    'password': 'SuperSecurePass123!', # Use your real password
    'host': 'terraform-20260423055542321500000003.cw5g0yus0fsb.us-east-1.rds.amazonaws.com', # Use your real endpoint
    'database': 'DEProjectDB'
}

try:
    print("Attempting to connect to RDS...")
    conn = mysql.connector.connect(**db_config)
    print("✅ SUCCESS! Your EC2 is talking to your RDS Database.")
    conn.close()
except Exception as e:
    print("❌ CONNECTION FAILED!")
    print(f"Error: {e}")
