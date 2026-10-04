import os
import socket
import datetime
from flask import Flask, request, render_template_string, redirect, url_for
import pymysql

app = Flask(__name__)

# RDS Database Configuration
DB_CONFIG = {
    'user': os.environ.get('DB_USER', 'admin'),
    'password': os.environ.get('DB_PASSWORD', 'SuperSecurePass123!'),
    'host': os.environ.get('DB_HOST', 'de-project-mysql-db.cw5g0yus0fsb.us-east-1.rds.amazonaws.com'),
    'database': os.environ.get('DB_NAME', 'DEProjectDB'),
    'connect_timeout': 5
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def init_db():
    """Initializes the database schema if it doesn't already exist."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                event_type VARCHAR(64) NOT NULL,
                details VARCHAR(255) NOT NULL,
                source_ip VARCHAR(45) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        # Insert a seed record if table is empty
        cursor.execute("SELECT COUNT(*) FROM audit_logs;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO audit_logs (event_type, details, source_ip)
                VALUES ('SYSTEM_INIT', 'Baseline Cryptographic Deployment Verified (KMS CMK)', '127.0.0.1');
            """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB INIT ERROR] {e}")

# Modern Enterprise Security Operations Dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Cloud Security Operations | DE Project</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090d16;
            --card-bg: rgba(17, 24, 39, 0.75);
            --border: rgba(255, 255, 255, 0.08);
            --border-hover: rgba(56, 189, 248, 0.3);
            --text-primary: #f8fafc;
            --text-muted: #94a3b8;
            --accent-cyan: #38bdf8;
            --accent-blue: #3b82f6;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --accent-amber: #f59e0b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 10% 20%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
                radial-gradient(at 90% 80%, rgba(59, 130, 246, 0.08) 0px, transparent 50%);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 32px 24px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Top Header */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 32px;
        }

        .brand-title {
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.5px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-badge {
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(56, 189, 248, 0.3);
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 9999px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .author-meta {
            font-size: 13px;
            color: var(--text-muted);
            text-align: right;
        }

        .author-meta strong {
            color: var(--text-primary);
        }

        /* Live Worker Telemetry Banner */
        .telemetry-banner {
            background: linear-gradient(90deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
            border: 1px solid var(--border);
            border-left: 4px solid var(--accent-cyan);
            padding: 16px 20px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
            backdrop-filter: blur(12px);
        }

        .telemetry-node {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px;
        }

        .pulse-dot {
            width: 10px;
            height: 10px;
            background-color: var(--accent-emerald);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent-emerald);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        /* 3-Tier Security Cards */
        .tier-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
            gap: 20px;
            margin-bottom: 36px;
        }

        .tier-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 20px;
            transition: all 0.25s ease;
            backdrop-filter: blur(10px);
        }

        .tier-card:hover {
            border-color: var(--border-hover);
            transform: translateY(-2px);
        }

        .tier-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .tier-num {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .tier-status {
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 6px;
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-emerald);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .tier-title {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .tier-desc {
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.5;
        }

        /* Two Column Layout */
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 24px;
            margin-bottom: 36px;
        }

        @media (max-width: 900px) {
            .content-grid { grid-template-columns: 1fr; }
        }

        .glass-panel {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(12px);
        }

        .panel-header {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Forms & Inputs */
        .form-group {
            margin-bottom: 16px;
        }

        label {
            display: block;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        input[type="text"], select {
            width: 100%;
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 14px;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
            transition: border 0.2s;
        }

        input[type="text"]:focus, select:focus {
            border-color: var(--accent-cyan);
        }

        .btn-submit {
            width: 100%;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            color: #041026;
            font-weight: 700;
            font-size: 14px;
            padding: 12px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: opacity 0.2s;
            margin-top: 8px;
        }

        .btn-submit:hover {
            opacity: 0.92;
        }

        /* Data Table */
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }

        th {
            text-align: left;
            padding: 12px 14px;
            color: var(--text-muted);
            font-weight: 600;
            border-bottom: 1px solid var(--border);
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.5px;
        }

        td {
            padding: 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-primary);
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }

        .event-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 4px;
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent-cyan);
            border: 1px solid rgba(56, 189, 248, 0.25);
        }

        .db-status-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid var(--border);
        }

        .db-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <div>
                <div class="brand-title">
                    🛡️ Automated Cloud Security Platform
                    <span class="brand-badge">Project II</span>
                </div>
            </div>
            <div class="author-meta">
                Course: <strong>977-302 Digital Engineering Project II</strong><br>
                Student: <strong>Aye Min Khant (6630613023)</strong>
            </div>
        </header>

        <!-- Live Infrastructure Node Banner -->
        <div class="telemetry-banner">
            <div class="telemetry-node">
                <div class="pulse-dot"></div>
                <span>Active Compute Node: <strong>{{ hostname }}</strong> (VPC Private App Tier)</span>
            </div>
            <div class="telemetry-node" style="color: var(--text-muted);">
                <span>Region: <strong>us-east-1</strong> | Multi-AZ ASG Fleet</span>
            </div>
        </div>

        <!-- 3-Tier Security Architecture (Aligned with Reference Architecture) -->
        <div class="tier-grid">
            <div class="tier-card">
                <div class="tier-header">
                    <span class="tier-num">Tier 1 • Public Ingress</span>
                    <span class="tier-status">WAF ACTIVE</span>
                </div>
                <div class="tier-title">ALB & AWS WAF v2</div>
                <div class="tier-desc">Public entry across AZ-1a/1b terminating port 80. Protected by AWS WAF v2 WebACL for Layer 7 inspection (OWASP Top 10, SQLi, and 100 req/5min rate limiting).</div>
            </div>

            <div class="tier-card">
                <div class="tier-header">
                    <span class="tier-num">Tier 2 • Private App</span>
                    <span class="tier-status">ISOLATED</span>
                </div>
                <div class="tier-title">Auto Scaling Compute</div>
                <div class="tier-desc">Zero public IPs. Multi-AZ private subnets executing self-healing Flask daemons managed by systemd (2 to 4 worker nodes).</div>
            </div>

            <div class="tier-card">
                <div class="tier-header">
                    <span class="tier-num">Tier 3 • Persistence</span>
                    <span class="tier-status">KMS ENCRYPTED</span>
                </div>
                <div class="tier-title">Air-Gapped RDS MySQL</div>
                <div class="tier-desc">Dedicated DB subnets with zero internet route. Hardened MySQL storage encrypted at rest via AWS KMS Customer Managed Key (CMK).</div>
            </div>
        </div>

        <!-- Main Workspace Grid -->
        <div class="content-grid">
            <!-- Left: Record Insertion Form -->
            <div class="glass-panel">
                <div class="panel-header">📝 Append Audit Event</div>
                <form action="/add-event" method="POST">
                    <div class="form-group">
                        <label for="event_type">Event Classification</label>
                        <select name="event_type" id="event_type">
                            <option value="USER_LOGIN">User Access Verification</option>
                            <option value="PERIMETER_CHECK">WAF Rule Verification</option>
                            <option value="DATA_PERSISTENCE">KMS Storage Audit</option>
                            <option value="COMPLIANCE_SCAN">CIS Benchmark Validation</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="details">Log Details / Payload</label>
                        <input type="text" name="details" id="details" placeholder="Enter log payload or description..." required>
                    </div>
                    <button type="submit" class="btn-submit">🔒 Secure Parameterized Write</button>
                </form>
            </div>

            <!-- Right: Live Database Table -->
            <div class="glass-panel">
                <div class="panel-header">🗄️ Persistence Tier (KMS Encrypted Storage)</div>
                {% if db_error %}
                    <div style="background: rgba(244, 63, 94, 0.15); border: 1px solid var(--accent-rose); color: var(--accent-rose); padding: 16px; border-radius: 8px; font-size: 13px;">
                        ⚠️ <strong>Database Connection Pending:</strong> {{ db_error }}
                    </div>
                {% else %}
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Classification</th>
                                <th>Payload Summary</th>
                                <th>Source IP</th>
                                <th>Timestamp (UTC)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in records %}
                            <tr>
                                <td style="font-family: 'JetBrains Mono', monospace; color: var(--text-muted);">#{{ row[0] }}</td>
                                <td><span class="event-tag">{{ row[1] }}</span></td>
                                <td>{{ row[2] }}</td>
                                <td style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-muted);">{{ row[3] }}</td>
                                <td style="font-size: 12px; color: var(--text-muted);">{{ row[4] }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% endif %}

                <div class="db-status-bar">
                    <div class="db-badge">
                        <span>Target: <strong>{{ db_host }}</strong></span>
                    </div>
                    <span>Encryption: <strong>AES-256 (KMS CMK)</strong></span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    init_db()
    hostname = socket.gethostname()
    records = []
    db_error = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, event_type, details, source_ip, created_at FROM audit_logs ORDER BY id DESC LIMIT 10;")
        records = cursor.fetchall()
        conn.close()
    except Exception as e:
        db_error = str(e)

    return render_template_string(
        HTML_TEMPLATE,
        hostname=hostname,
        records=records,
        db_error=db_error,
        db_host=DB_CONFIG['host']
    )

@app.route('/add-event', methods=['POST'])
def add_event():
    event_type = request.form.get('event_type', 'GENERAL_EVENT')
    details = request.form.get('details', '')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Secure Parameterized Query
        cursor.execute(
            "INSERT INTO audit_logs (event_type, details, source_ip) VALUES (%s, %s, %s);",
            (event_type, details, client_ip)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[INSERT ERROR] {e}")

    return redirect(url_for('index'))

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
