import smtplib
from email.message import EmailMessage

msg = EmailMessage()

def send(data,reciever=None):
    data = data + "\n\nThis message is sent from iNote.\n\n"
    msg.set_content(data)
    msg['From'] = "yourMail@gmail.com"

    if reciever is  None:
        msg['Subject'] = 'iNote - someone want to contact with you'
        msg['To'] = "recieverMail@gmail.com"
    else:
        msg['Subject'] = 'iNote - OTP'
        msg['To'] = reciever

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("yourMail@gmail.com", "yourpassword")
    server.send_message(msg)
    server.quit()
    del(msg['To'])
    del(msg['From'])
    del(msg['Subject'])
    
