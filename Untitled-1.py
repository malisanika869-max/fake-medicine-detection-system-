# ===============================================================
# FULL MIX CODE
# Advanced Fake Medicine Detection System
# Register + Login + SQLite
# Dashboard
# Name Verification
# QR Camera Verification
# Blockchain
# 50 Medicines + 50 QR
# ===============================================================

from flask import Flask, render_template_string, request, redirect, session
import sqlite3
import hashlib
import datetime

app = Flask(__name__)
app.secret_key = "medsecure"

# ===============================================================
# DATABASE
# ===============================================================

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ===============================================================
# BLOCKCHAIN
# ===============================================================

class Block:
    def __init__(self,index,data,prev_hash):
        self.index=index
        self.data=data
        self.prev_hash=prev_hash
        self.time=str(datetime.datetime.now())
        self.hash=self.make_hash()

    def make_hash(self):
        txt=str(self.index)+self.data+self.prev_hash+self.time
        return hashlib.sha256(txt.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain=[self.genesis()]

    def genesis(self):
        return Block(0,"GENESIS","0")

    def last(self):
        return self.chain[-1]

    def add(self,data):
        b=Block(len(self.chain),data,self.last().hash)
        self.chain.append(b)

chain = Blockchain()

# ===============================================================
# 50 MEDICINES
# ===============================================================

medicines = {
"paracetamol":"QR001","crocin":"QR002","dolo650":"QR003",
"aspirin":"QR004","cetirizine":"QR005","amoxicillin":"QR006",
"azithromycin":"QR007","metformin":"QR008","ibuprofen":"QR009",
"panadol":"QR010","combiflam":"QR011","sinarest":"QR012",
"digene":"QR013","eno":"QR014","gelusil":"QR015",
"calpol":"QR016","vicks":"QR017","benadryl":"QR018",
"norflox":"QR019","ofloxacin":"QR020","pantoprazole":"QR021",
"rabeprazole":"QR022","omeprazole":"QR023","zincovit":"QR024",
"becosules":"QR025","liv52":"QR026","neurobion":"QR027",
"augmentin":"QR028","disprin":"QR029","limcee":"QR030",
"monteklc":"QR031","wikoryl":"QR032","cipladine":"QR033",
"volini":"QR034","moov":"QR035","saridon":"QR036",
"shelcal":"QR037","ors":"QR038","electral":"QR039",
"dolonex":"QR040","taxim":"QR041","cefspan":"QR042",
"acyclovir":"QR043","nicip":"QR044","zerodol":"QR045",
"ultracet":"QR046","novamox":"QR047","lanzol":"QR048",
"ranitidine":"QR049","supradyn":"QR050"
}

# ===============================================================
# STYLE
# ===============================================================

style = """
<style>
body{
margin:0;
font-family:Arial;
background:linear-gradient(135deg,#0f172a,#1e293b);
color:white;
}
.top{
padding:18px;
text-align:center;
font-size:30px;
font-weight:bold;
background:#111827;
}
.box{
width:90%%;
max-width:720px;
margin:auto;
margin-top:35px;
padding:30px;
border-radius:22px;
background:rgba(255,255,255,0.08);
box-shadow:0 0 25px rgba(0,0,0,0.4);
}
input{
width:100%%;
padding:14px;
margin-top:10px;
margin-bottom:15px;
border:none;
border-radius:10px;
font-size:16px;
}
button{
width:100%%;
padding:14px;
background:#22c55e;
border:none;
color:white;
font-size:17px;
border-radius:10px;
cursor:pointer;
}
button:hover{background:#16a34a;}
a{
color:#38bdf8;
text-decoration:none;
margin:10px;
font-weight:bold;
}
.menu{text-align:center;margin-top:18px;}
.card{
padding:18px;
border-radius:14px;
background:rgba(255,255,255,0.08);
margin-top:12px;
text-align:center;
}
.good{
background:#14532d;
padding:18px;
border-radius:14px;
color:#86efac;
}
.bad{
background:#7f1d1d;
padding:18px;
border-radius:14px;
color:#fecaca;
}
</style>

<script src="https://unpkg.com/html5-qrcode"></script>
"""

# ===============================================================
# LOGIN + REGISTER
# ===============================================================

@app.route("/", methods=["GET","POST"])
def login():

    msg=""

    if request.method=="POST":

        action=request.form["action"]
        username=request.form["username"]
        password=request.form["password"]

        conn=sqlite3.connect("users.db")
        cur=conn.cursor()

        if action=="register":

            try:
                cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username,password)
                )
                conn.commit()
                msg="<p style='color:lightgreen;'>Registration Successful</p>"
            except:
                msg="<p style='color:red;'>Username Already Exists</p>"

        if action=="login":

            cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
            )

            user=cur.fetchone()

            if user:
                session["user"]=username
                conn.close()
                return redirect("/dashboard")
            else:
                msg="<p style='color:red;'>Invalid Login</p>"

        conn.close()

    return render_template_string(f"""
    <html><head>{style}</head><body>

    <div class='top'>Medicine Security System</div>

    <div class='box'>
    <h2>Register / Login</h2>

    <form method='post'>

    <input type='text' name='username' placeholder='Username' required>

    <input type='password' name='password' placeholder='Password' required>

    <button name='action' value='login'>Login</button>

    <br><br>

    <button name='action' value='register'
    style='background:#2563eb;'>Register</button>

    </form>

    {msg}

    </div>

    </body></html>
    """)

# ===============================================================
# DASHBOARD
# ===============================================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    return render_template_string(f"""
    <html><head>{style}</head><body>

    <div class='top'>Dashboard</div>

    <div class='box'>

    <div class='card'><a href='/name'>Medicine Name Verification</a></div>

    <div class='card'><a href='/qr'>QR Camera Verification</a></div>

    <div class='card'><a href='/logout'>Logout</a></div>

    </div>

    </body></html>
    """)

# ===============================================================
# NAME VERIFY
# ===============================================================

@app.route("/name", methods=["GET","POST"])
def name():

    if "user" not in session:
        return redirect("/")

    result=""

    if request.method=="POST":

        med=request.form["medicine"].lower()

        if med in medicines:

            chain.add(med)
            b=chain.last()

            result=f"""
            <div class='good'>
            Genuine Medicine<br><br>
            Name : {med.title()}<br>
            QR : {medicines[med]}<br>
            Block : {b.index}
            </div>
            """

        else:
            result="<div class='bad'>Fake Medicine</div>"

    return render_template_string(f"""
    <html><head>{style}</head><body>

    <div class='top'>Name Verification</div>

    <div class='box'>

    <form method='post'>
    <input type='text' name='medicine' placeholder='Enter Medicine Name' required>
    <button>Verify</button>
    </form>

    {result}

    <div class='menu'><a href='/dashboard'>Dashboard</a></div>

    </div>

    </body></html>
    """)

# ===============================================================
# QR PAGE
# ===============================================================

@app.route("/qr")
def qr():

    if "user" not in session:
        return redirect("/")

    return render_template_string(f"""
    <html><head>{style}</head><body>

    <div class='top'>QR Camera Verification</div>

    <div class='box'>

    <div id='reader'></div>

    <div id='result' class='card'>Open Camera & Scan QR</div>

    <div class='menu'><a href='/dashboard'>Dashboard</a></div>

    </div>

<script>

function success(decodedText){{
fetch("/verify_qr",{{
method:"POST",
headers:{{"Content-Type":"application/x-www-form-urlencoded"}},
body:"qr="+decodedText
}})
.then(response=>response.text())
.then(data=>{{
document.getElementById("result").innerHTML=data;
}});
}}

let scanner = new Html5QrcodeScanner(
"reader",
{{fps:10,qrbox:250}}
);

scanner.render(success);

</script>

    </body></html>
    """)

# ===============================================================
# VERIFY QR
# ===============================================================

@app.route("/verify_qr", methods=["POST"])
def verify_qr():

    qr=request.form["qr"]

    for name,code in medicines.items():

        if code==qr:

            chain.add(qr)
            b=chain.last()

            return f"""
            <div class='good'>
            Genuine QR<br><br>
            Name : {name.title()}<br>
            QR : {qr}<br>
            Block : {b.index}
            </div>
            """

    return "<div class='bad'>Fake QR Code</div>"

# ===============================================================
# LOGOUT
# ===============================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ===============================================================
# RUN
# ===============================================================

if __name__ == "__main__":
    app.run(debug=True)