import os
import smtplib
from email.message import EmailMessage

from datetime import datetime

email = 'romashmlc@gmail.com'
password = 'xpkcbnpnkzbrvtmv'


def send_mail(to, token, username, email=email, password=password):
    msg = EmailMessage()
    msg.add_alternative(
        f"""\
<html lang="en">
<body>
    <section>
        <nav class="Platform">
            <div class="Border">
            <p class="GlobalFinance Montserrat"> Global Finance inc. </p>
            </div>
            <div class="manage">
            <div class="Border">
                <p class="LocalTime Montserrat"> {datetime.now().strftime("%H:%M")} MSC </p>
            </div>
            </div>
        </nav>
        <div class="flexbox-center-signup">
            <p class="Enterence Montserrat">
                К вам на сервер хочет попасть {username}
            </p>
            <p class="Enterence Montserrat">
                Его email - {email}, если вам человек не знаком проигнорируйте сообщение. В ином случае <a href="http://localhost:8000/verify/{token}">
                    нажмите
                </a>
            </p>
        </div>
    </body>
</html>
<style>
    /* Imports fonts */

    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@100&display=swap');
    .Montserrat {{font-family: 'Montserrat', sans-serif;}}
    
    body {{
        margin: 0;
        padding: 0;
        background: url('../static/images/blob-scene-haikei.jpeg') no-repeat ;
        background-size: cover;
        height: 100%;
    }}
    
    .Platform {{
        max-width: 100%;
        height: auto;
        display: flex;
        align-items: center;
        padding-top: 2%;
        justify-content: space-around;
    }}
    
    .Border {{
        background-color: #fbfbfb;
        width: auto;
        height: auto;   
        padding-left: 3%; 
        padding-right: 3%;  
    
    }}
    
    .GlobalFinance {{
        font-size: 42px;
        margin-bottom: 0;
    }}
    
    .manage {{
        width: 30%;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding-left: 10%;
    }}
    
    .LocalTime {{
        font-size: 28px;
        display: flex;
        justify-content: center;
        align-items: center;
        white-space: nowrap;
        margin-bottom: 0;
    }}
    
    .userAccountSite {{
        display: flex;
        padding-left: 10%;
    }}
    
    .turnoff {{
        display: flex;
        padding-left: 10%;
        background: url('../static/images/turnoff.svg') no-repeat ;
        background-size: contain;
        width: 50px;
        height: 50px;
        border: none;
        cursor: pointer;
        outline: none;
    }}

    .Enterence {{
        font-size: 26px;
        background-color: #fbfbfb;
        padding-left: 1%;
        padding-right: 1%;
    
        width: auto;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }}

    .flexbox-center-signup {{
        width: 100%;
        display: flex;
        justify-content: center;
        text-align: center;
        flex-direction: column;
    
        padding-top: 5%;
    }}
</style>
    """,
        subtype="html",
    )

    msg["Subject"] = "Добро пожаловать в Global Finance"
    msg["From"] = email
    msg["To"] = to

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email, password)
    server.send_message(msg)
    server.quit()