import socket

targets = []

def processMessage(name, role):
	fileContents = ''
	with open('./emailTemplate.txt', 'r') as email:
		for line in email.readlines():
			if '$NAME' in line:
				line.replace('$NAME', name)
			if '$ROLE' in line:
				line.replace('$ROLE', role)

			fileContents += line

	return fileContents

def collectCampaignTargets():
	global targets
	with open('./targets.csv', 'r') as targets:
		for line in targets.readlines():
			email = line.split[0]
			name = line.split[1]
			role = line.split[2]
			targets.append((email, name, role))

def sendMail(email, name, role, server, content, port=25):
	from = 'coolguy@dropbox.com'
	connection = socket.socket(socket.SOCK_STREAM, socket.AF_INET)
	connection.connect((server, port))

	connection.send('HELO JOE\r\n')
	response = connection.recv(1024)
	print(response)

	connection.send(f'MAIL FROM: {from}\r\n')
	response = connection.recv(1024)
	print(response)

	connection.send(f'RCPT TO: {email}\r\n')
	response = connection.recv(1024)
	print(response)

	connection.send('DATA\r\n')
	response = connection.recv(1024)
	print(response)

	connection.send('SUBJECT: test emailer\r\n\r\n')
	with open(emailTemplate.txt) as message:
		for line in message.readlines():
			connection.send(f'\r\n {line}')
	connection.send('\r\n.\r\n')
	response = connection.recv(1024)
	print(response)

	connection.send('QUIT\r\n')
	response = connection.recv(1024)
	print(response)

	connection.close()


def main():
	mailServer = input('Enter mailServer: ')
	port = input('Enter port mailServer runs on: ')
	collectCampaignTargets()

	for target in targest:
		content = processMessage(target[1], target[2])
		sendMail(target[0], target[1], target[2],mailServer,content,int(port))
	

if __name__ == '__main__':
	main()