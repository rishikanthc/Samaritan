import nexmo

replyClient = nexmo.Client(key='3675d142',secret='a0eab3f1295ce225')

# number = raw_input('Enter the phone number: ')
# message = raw_input('Enter the message: ')

def send_sms(number, message):
	response = replyClient.send_message({'from' : '12034869034', 'to' : number, 'text' : message })
	response = response['messages'][0]
	if response['status'] == '0':
		print 'Send message ', response['message-id']
	else:
		print 'Error: ', response['error-text']
