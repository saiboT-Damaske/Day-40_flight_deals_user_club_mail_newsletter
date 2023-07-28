import requests
import smtplib

TELEGRAM_API = 'https://api.telegram.org/bot'
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

GMAIL_USER = ""
GMAIL_PW = ""


class NotificationManager:

    def send_low_price_alert(self, message):
        bot_token = TELEGRAM_BOT_TOKEN
        bot_chat_id = TELEGRAM_CHAT_ID
        send_text = TELEGRAM_API \
                    + bot_token \
                    + "/sendMessage?chat_id=" \
                    + bot_chat_id \
                    + "&parse_mode=Markdown&text=" \
                    + message

        telegram_response = requests.get(send_text)
        print(telegram_response.text)


    def send_club_member_deals(self, to_email, message):

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=GMAIL_USER, password=GMAIL_PW)
            connection.sendmail(from_addr=GMAIL_USER, to_addrs=to_email, msg=message)


