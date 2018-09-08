from twilio.rest import Client

account_sid = 'ACa209e1ae289d60729d7321952c4d8974'
auth_token = '483d41d0e680edbfa018d0f0cfc6c578'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+12672146320',
                              body='hi this is a test',
                              to='+14165539697'
                          )

<<<<<<< HEAD
print(message.sid)uio 
=======
print(message.sid)
>>>>>>> 334415ce8a7baad51e0eccaa638ffb09622dcdd5
