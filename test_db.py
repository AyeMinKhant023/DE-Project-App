import mysql.connector

# YOUR DATABASE INFO
db_config = {
    'user': 'admin',
    'password': 'SuperSecurePass123!', # hide password later
    'host': 'terraform-20260429093317123700000002.cw5g0yus0fsb.us-east-1.rds.amazonaws.com', # (RDS -> Databases -> Connectivity & security -> Endpoints -> Endpoint & port -> copy under Endpoint)
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
