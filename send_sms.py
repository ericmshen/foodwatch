from twilio.rest import Client

account_sid = '<INSERT SID HERE>'
auth_token = '<INSERT AUTH TOKEN HERE>'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              from_='+12672146320',
                              body='soylent',
                              to=''
                          )

print(message.sid)
