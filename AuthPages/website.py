from flask import Flask, request
from AuthPages.dbConnection import connectionDB
from AuthPages.tools import email_send

app = Flask(__name__)

@app.route("/")
def confirmation() -> str:
    mail = request.args.get('email')
    code = request.args.get('code')
    code = connectionDB(mail, code)
    email_send(mail, code)

    s = f'''<html>
    <body style="background: #eee !important;">
    <div style="margin-top: 80px;margin-bottom: 80px;">
    <form style="max-width: 380px;padding: 15px 35px 45px;margin: 0 auto;background-color: #fff;border: 1px solid rgba(0,0,0,0.1);">
      <h3>Thanks for allowing the guest connecting to the school WiFi we sent him the code in the Email {mail}</h3> 
    </form>
    </div>
    </body>
    </html>'''
    return s


if __name__ == "__main__":
    app.run(debug=False)

