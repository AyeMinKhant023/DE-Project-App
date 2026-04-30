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
    cursor = conn.cursor()
    print("✅ SUCCESS! Your EC2 is talking to your RDS Database.")

    # 1. Create a Table (Integrity Test)
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
    
    # 2. INSERT data using the SECURE Parameterized method
    student_name = "Patric_Student"
    sql = "INSERT INTO students (name) VALUES (%s)" # The %s is the 'Shield'
    cursor.execute(sql, (student_name,)) # We pass the data separately

    conn.commit()
    print(f"✅ INTEGRITY TEST: Successfully inserted '{student_name}' using Parameterized Query.")

    cursor.close()
    conn.close()
except Exception as e:
    print("❌ CONNECTION FAILED!")
    print(f"Error: {e}")
