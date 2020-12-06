import slack
from slackeventsapi import SlackEventAdapter
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
import metaweather
from datetime import datetime, timedelta
from dayforecastobject import BlockBuilder, CityForecast
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

client.chat_postMessage(channel=os.environ['CHANNEL_NAME'], text="Živ sam!")
BOT_ID = client.api_call("auth.test")['user_id']

welcome_messages = {}

SCHEDULED_MESSAGES = [
    {'text': 'First message', 'post_at': (datetime.now() + timedelta(seconds=20)).timestamp(),
     'channel': 'C01F6GNPL3F'},
    {'text': 'Second Message!', 'post_at': (datetime.now() + timedelta(seconds=30)).timestamp(),
     'channel': 'C01F6GNPL3F'}
]


def daily_weather_report():
    user_id = 'U01EUSL128P'
    client.chat_postMessage(channel=user_id, text="DM with interval!")


def send_tomorrow_forecast(channel):
    weather_response = metaweather.get_forecast().json()
    block_builder = BlockBuilder(CityForecast(weather_response), channel)
    message_forecast = block_builder.get_tomorrow_forecast()
    response = client.chat_postMessage(**message_forecast)
    # https://stackoverflow.com/questions/36901/what-does-double-star-asterisk-and-star-asterisk-do-for-parameters


def send_week_forecast(channel):
    weather_response = metaweather.get_forecast().json()
    block_builder = BlockBuilder(CityForecast(weather_response), channel)
    message_forecast = block_builder.get_week_forecast()
    response = client.chat_postMessage(**message_forecast)


# https://stackoverflow.com/questions/6392739/what-does-the-at-symbol-do-in-python
@slack_event_adapter.on('message')
def message(payLoad):
    print("Message PAYLOAD:")
    print(payLoad)
    event = payLoad.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if text[0] == '!':
        option = text[1:].lower()
        if option == 'help':
            client.chat_postMessage(channel=channel_id,
                                    text='Upiši:\n*!sutra* za sutrašnju prognozu\n*!tjedan* za tjednu prognozu')
        elif option == 'sutra':
            send_tomorrow_forecast(channel=channel_id)

        elif option == 'tjedan':
            send_week_forecast(channel=channel_id)

        else:
            client.chat_postMessage(channel=channel_id,
                                    text='Izgleda da upisuješ krivu naredbu, probaj *!help*')


# slash command for city forecast change
@app.route('/grad', methods=['POST'])
def message_count():
    data = request.form  # 3- 5.55
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    print(text)

    if text == '':
        client.chat_postMessage(channel=channel_id, text='Nedostaje argument #ime-grada')
    else:
        # promjeni grad
        client.chat_postMessage(channel=channel_id, text='Grad promjenjen u ' + text)

    return Response(), 200


cron = BackgroundScheduler(daemon=True)
cron.add_job(func=daily_weather_report, trigger='cron', minute='*')  # staviti hour='20'- možda staviti kao parametar?
cron.start()

atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == "__main__":
    # ids = schedule_messages(SCHEDULED_MESSAGES)
    app.run(debug=True)
