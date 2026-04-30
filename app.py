from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# Your secure infrastructure connection
db_config = {
    'user': 'admin',
    'password': 'SuperSecurePass1234!', 
    'host': 'terraform-20260429093317123700000002.cw5g0yus0fsb.us-east-1.rds.amazonaws.com',
    'database': 'DEProjectDB'
}

# The HTML for your website front-end
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>DE Project - Security Test</title></head>
<body style="font-family: Arial; margin: 40px;">
    <h2>Automated Cloud Security - Application Layer Test</h2>
    
    <div style="background-color: #f4f4f4; padding: 20px; border-radius: 5px;">
        <h3>Register New Student</h3>
        <form method="POST" action="/add">
            <label>Student Name (Try to hack me!):</label><br><br>
            <input type="text" name="student_name" size="60" placeholder="e.g., Patric OR '; DROP TABLE students; --" required><br><br>
            <input type="submit" value="Submit to Database" style="background-color: #007BFF; color: white; padding: 10px; border: none;">
        </form>
    </div>

    <h3>Current Database State (students table):</h3>
    <ul>
    {% for student in students %}
        <li><strong>ID:</strong> {{ student[0] }} | <strong>Name:</strong> {{ student[1] }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def home():
    # Fetch all current data to show on the screen
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    
    return render_template_string(HTML_PAGE, students=students)

@app.route('/add', methods=['POST'])
def add_student():
    # 1. Receive data from the external web form
    user_input = request.form['student_name']
    
    # 2. Connect to RDS
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 3. SCENARIO 3: The Integrity Shield (%s)
    sql = "INSERT INTO students (name) VALUES (%s)"
    cursor.execute(sql, (user_input,))
    
    conn.commit()
    conn.close()

    # Refresh the page to show the result
    return "<script>window.location.href='/';</script>"

if __name__ == '__main__':
    # Listen on all public IPs so you can reach it from your MacBook
    app.run(host='0.0.0.0', port=5000)