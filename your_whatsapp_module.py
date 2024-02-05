from twilio.rest import Client


def send_whatsapp_message(to_number, message):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Twilio WhatsApp number
        to='whatsapp:' + to_number
    )
