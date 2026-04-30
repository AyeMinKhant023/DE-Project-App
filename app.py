# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "<h1>Welcome to Automated Cloud Security Project</h1>" \
#     "<p>✅ AWS server by Patric is Running!</p>" \
#     "<p>✅ Database connection is successful!</p>"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# Ensure your password and host are exactly correct here
db_config = {
    'user': 'admin',
    'password': 'SuperSecurePass123!', 
    'host': 'terraform-20260429093317123700000002.cw5g0yus0fsb.us-east-1.rds.amazonaws.com',
    'database': 'DEProjectDB'
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>DE Project - Security Test</title></head>
<body style="font-family: Arial; margin: 40px; line-height: 1.6;">
    <h2 style="color: #2c3e50;">Automated Cloud Security - Application Layer</h2>
    
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #dee2e6;">
        <h3 style="margin-top: 0;">Target: Data Integrity Test</h3>
        <p>Attempt to bypass the database parameters using a malicious payload.</p>
        <form method="POST" action="/add">
            <label style="font-weight: bold;">Simulated User Input:</label><br><br>
            <input type="text" name="student_name" style="width: 100%; padding: 10px; max-width: 500px;" placeholder="e.g., Patric OR '; DROP TABLE students; --" required><br><br>
            <input type="submit" value="Execute Payload" style="background-color: #007BFF; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">
        </form>
    </div>

    <h3>Current Database State (students table):</h3>
    <ul style="background: #e9ecef; padding: 20px; border-radius: 8px;">
    {% if error %}
        <li style="color: red;"><strong>Database Error:</strong> {{ error }}</li>
    {% elif students %}
        {% for student in students %}
            <li><strong>ID:</strong> {{ student[0] }} | <strong>Record:</strong> {{ student[1] }}</li>
        {% endfor %}
    {% else %}
        <li>No records found or table does not exist yet.</li>
    {% endif %}
    </ul>
</body>
</html>
"""

@app.route('/')
def home():
    students = []
    error_msg = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Ensure table exists before querying
        cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()
    except Exception as e:
        error_msg = str(e)
        
    return render_template_string(HTML_PAGE, students=students, error=error_msg)

@app.route('/add', methods=['POST'])
def add_student():
    user_input = request.form['student_name']
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # SCENARIO 3: The Integrity Shield (%s)
        sql = "INSERT INTO students (name) VALUES (%s)"
        cursor.execute(sql, (user_input,))
        
        conn.commit()
        conn.close()
    except Exception as e:
        return f"<h3>Application Error Caught:</h3><p>{e}</p><a href='/'>Return to Application</a>"

    return "<script>window.location.href='/';</script>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)