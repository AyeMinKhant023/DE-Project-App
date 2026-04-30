from flask import Flask, request, render_template_string, redirect
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'admin',
    'password': 'SuperSecurePass123!',
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
        <div style="flex: 1; background: white; padding: 20px; border-top: 5px solid green; border-radius: 8px;">
            <h3 style="color: green;">Category A: Secure Path (%s)</h3>
            <p><small>Uses Parameterized Queries. Input is treated strictly as <b>Data</b>.</small></p>
            <form method="POST" action="/secure-add">
                <input type="text" name="name" style="width: 80%;" placeholder="Type normal name OR payload" required><br><br>
                <input type="submit" value="Secure Insert" style="background: green; color: white; border: none; padding: 10px; cursor: pointer;">
            </form>
        </div>
        <div style="flex: 1; background: white; padding: 20px; border-top: 5px solid red; border-radius: 8px;">
            <h3 style="color: red;">Category B: Vulnerable Path (f-string)</h3>
            <p><small>Uses String Concatenation. Input can be interpreted as <b>Instructions</b>.</small></p>
            <form method="POST" action="/vulnerable-add">
                <input type="text" name="name" style="width: 80%;" placeholder="Type normal name OR payload" required><br><br>
                <input type="submit" value="Vulnerable Insert" style="background: red; color: white; border: none; padding: 10px; cursor: pointer;">
            </form>
        </div>
    </div>

    <h3>Current Database State:</h3>
    {% if table_missing %}
        <div style="background: #ffcccc; padding: 20px; border: 2px solid red; border-radius: 8px; color: red;">
            <h2>🚨 CRITICAL AVAILABILITY LOSS 🚨</h2>
            <p><b>Error: Table 'students' does not exist!</b></p>
            <p>The database table was successfully dropped by a malicious payload.</p>
        </div>
    {% else %}
        <table border="1" style="width: 100%; background: white; text-align: left;">
            <tr><th style="padding: 10px;">ID</th><th style="padding: 10px;">Record Content (The Data)</th></tr>
            {% for student in students %}
            <tr><td style="padding: 10px;">{{ student[0] }}</td><td style="padding: 10px;">{{ student[1] }}</td></tr>
            {% endfor %}
        </table>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    students = []
    table_missing = False
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()
    except Exception:
        table_missing = True

    return render_template_string(HTML_PAGE, students=students, table_missing=table_missing)


# --- CATEGORY A (SECURE) ---
@app.route('/secure-add', methods=['POST'])
def secure():
    val = request.form['name']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (%s)", (val,))
        conn.commit()
        conn.close()
    except Exception:
        pass
    return redirect('/')


# --- CATEGORY B (VULNERABLE) ---
@app.route('/vulnerable-add', methods=['POST'])
def vulnerable():
    val = request.form['name']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = f"INSERT INTO students (name) VALUES ('{val}')"
        results = cursor.execute(sql, multi=True)
        for result in results:
            try:
                result.fetchall()
            except Exception:
                pass
        conn.commit()
        conn.close()
    except Exception:
        pass
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)