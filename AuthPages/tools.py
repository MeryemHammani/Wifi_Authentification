import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#tools to generate code and send email
def generate_code(length):
    letters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(letters) for i in range(length))
    return code

def send_email_structure(toaddr,subject,body,body_type):
        fromaddr = 'hammani.meryem29@gmail.com'
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] =subject

        msg.attach(MIMEText(body, body_type))

        server = smtplib.SMTP('smtp.gmail.com', 25)
        server.starttls()
        server.login(fromaddr, 'xhdamwegwsuigddl')
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        # gbtxhwvytjejpnhn

def email_guest(toaddr ,guest,code):
        link = f'http://127.0.0.1:5000?email={guest}&code={code}'
        style = '''display: inline-block;
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px 20px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    border-radius: 5px;
                    border: none;
                    cursor: pointer; '''
        href = f'<a href="{link}" style="{style}" target="_self" class="button-link">Accept</a>'
        html_body =f'''<html>
        <head>
        </head>
        <body>
        <h1 style='color:#CC00CC'>Connection permission</h1>
        <p>Click the button below to give the person who has the email {guest} the permission to connect
         to the school WiFi<br>if this email appears by mistake ignore it</p>
        {href}
        </body>
        </html>'''
        send_email_structure(toaddr, 'Access Permission', html_body, 'html')

def email_send(toaddr,code):
       send_email_structure(toaddr, 'Your Password', f'to connect to the WiFi enter the code:{code}', 'plain')

