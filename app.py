from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'admin',
    'password': 'SuperSecurePass123!', # Ensure this matches your Terraform password
    'host': 'terraform-20260429093317123700000002.cw5g0yus0fsb.us-east-1.rds.amazonaws.com',
    'database': 'DEProjectDB'
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Cloud Security Lab</title></head>
<body style="font-family: sans-serif; margin: 40px; background-color: #f0f2f5;">
    <h2>DE Project: Automated Cloud Security Verification</h2>
    
    <div style="display: flex; gap: 20px;">
        <!-- CATEGORY A: THE SECURE SHIELD -->
        <div style="flex: 1; background: white; padding: 20px; border-top: 5px solid green; border-radius: 8px;">
            <h3 style="color: green;">Category A: Secure Path (%s)</h3>
            <p><small>Uses Parameterized Queries. Input is treated strictly as <b>Data</b>.</small></p>
            <form method="POST" action="/secure-add">
                <input type="text" name="name" style="width: 80%;" placeholder="Try '; DROP TABLE students; --" required><br><br>
                <input type="submit" value="Secure Insert" style="background: green; color: white; border: none; padding: 10px;">
            </form>
        </div>

        <!-- CATEGORY B: THE VULNERABLE HOLE -->
        <div style="flex: 1; background: white; padding: 20px; border-top: 5px solid red; border-radius: 8px;">
            <h3 style="color: red;">Category B: Vulnerable Path (f-string)</h3>
            <p><small>Uses String Concatenation. Input can be interpreted as <b>Instructions</b>.</small></p>
            <form method="POST" action="/vulnerable-add">
                <input type="text" name="name" style="width: 80%;" placeholder="Try '; DROP TABLE students; --" required><br><br>
                <input type="submit" value="Vulnerable Insert" style="background: red; color: white; border: none; padding: 10px;">
            </form>
        </div>
    </div>

    <h3>Database Records:</h3>
    <table border="1" style="width: 100%; background: white;">
        <tr><th>ID</th><th>Record Content (The Data)</th></tr>
        {% for student in students %}
        <tr><td>{{ student[0] }}</td><td>{{ student[1] }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def home():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_PAGE, students=students)

# THE SECURE BUTTON LOGIC
@app.route('/secure-add', methods=['POST'])
def secure():
    val = request.form['name']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name) VALUES (%s)", (val,)) # THE SHIELD
    conn.commit()
    conn.close()
    return "<script>window.location.href='/';</script>"

# THE VULNERABLE BUTTON LOGIC
@app.route('/vulnerable-add', methods=['POST'])
def vulnerable():
    val = request.form['name']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    # THE VULNERABILITY: Directly injecting string and allowing multiple commands
    sql = f"INSERT INTO students (name) VALUES ('{val}')"
    for result in cursor.execute(sql, multi=True):
        pass
    conn.commit()
    conn.close()
    return "<script>window.location.href='/';</script>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)