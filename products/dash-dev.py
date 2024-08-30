from flask import Flask, render_template, request
import subprocess
import re
from flask_httpauth import HTTPDigestAuth
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '8337rxm83497xrm83249xt78f387uifup30u84u8u348f3pq4jf'
auth = HTTPDigestAuth()

users = {
    "user": "password",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

@app.route('/')
@auth.login_required
def hello_name():
   return render_template('index.html')
   #return out

@app.route('/api',methods = ['POST', 'GET'])
@auth.login_required
def tbd():
   url = str(request.form['url'])
   cat = str(request.form['cat'])
   cmd = ["python/bin/python3","temu.py", url, cat]
   print(cmd)
   #os.system(cmd)
   x = subprocess.Popen(cmd, stdout=subprocess.PIPE)
   out, err = x.communicate()
   esc = escape_ansi(out.decode())
   if err:
      status = "Import Failed!"
   elif "fka;skf" in esc:
      status = "Failed!"
   else:
      status = "Success!"
   return render_template('executed.html', status=status,output=esc)
   #return out
@app.route('/cmd')
@auth.login_required
def exec():
   return render_template('cmd.html')
   #return out

@app.route('/ip')
@auth.login_required
def ip():
   return render_template('ip.html')
   #return out

if __name__ == '__main__':
   #x = subprocess.Popen('ls', stdout=subprocess.PIPE)
   #out, err = x.communicate()
   #print(out)
   app.run(host='0.0.0.0', debug = True)
   #app.run(host="192.168.0.3",debug = False, ssl_context= ('cert.pem', 'key.pem'))
