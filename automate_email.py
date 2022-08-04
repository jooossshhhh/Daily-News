# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 08:27:46 2022

@author: josh.smith
"""

import smtplib
from email.message import EmailMessage



def email_alert(subject,body,alternative,recipients):
    for recipient in recipients:

        msg = EmailMessage()
        msg.set_content(body)
    #     msg.add_alternative("""<pre> 
    # Congratulations! We've successfully created account.
    # Go to the page: <a href="https://www.google.com/">click here</a>
    # Thanks,
    # XYZ Team.
    # </pre>""",subtype = 'html')
        if alternative:
            msg.add_alternative(alternative,'html')
        msg['subject'] = subject
        
        msg['to'] = recipient
        
        user = your_email
        password = your_password
        msg['from'] = user
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user,password)
        server.send_message(msg)
        server.quit()

if __name__ == '__main__':

    print('now sending message...')
    email_alert('testing','test',None, test_email)
    email_alert('testing','this wont send','this will send', test_email)