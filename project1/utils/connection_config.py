import smtplib
from email.mime.text import MIMEText

from fastapi import HTTPException

def send_reset_email(email:str,access_token:str):
    smtp_server="smtp.gmail.com"
    smtp_port=587
    smtp_username="sohamghayal02@gmail.com"
    smtp_password="tzfnbfojcoodxsil"
    sender_email="sohamghayal02@gmail.com"
    
    subject="Password reset"
    body=f"your reset_token is:{access_token} and for reset password click: http://192.168.130.41:8000/reset_password/"
    
    
    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=sender_email
    msg['To']=email
    
    try:
        with smtplib.SMTP(smtp_server,smtp_port) as server:
            server.starttls()
            server.login(smtp_username,smtp_password)
            server.sendmail(sender_email,[email],msg.as_string())
            print("email_sent")
    except:
        raise HTTPException(status_code=500,detail="failed")