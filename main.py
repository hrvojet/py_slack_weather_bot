import slack
import os
import metaweather
import atexit
from slackeventsapi import SlackEventAdapter
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from dayforecastobject import BlockBuilder, CityForecast
from apscheduler.schedulers.background import BackgroundScheduler

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']


def daily_weather_report():
    channel = 'U01EUSL128P'
    # client.chat_postMessage(channel=channel, text=":sunny:")
    weather_response = metaweather.get_forecast().json()
    block_builder = BlockBuilder(CityForecast(weather_response), channel)
    message_forecast = block_builder.tomorrow_report()
    response = client.chat_postMessage(**message_forecast)


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


cron = BackgroundScheduler(daemon=True)
cron.add_job(func=daily_weather_report, trigger='cron', hour='*', minute='*')  # demo
# cron.add_job(func=daily_weather_report, trigger='cron', hour='20', minute='0')
cron.start()
cron.print_jobs()
print("scheduler jobs:")
print(cron.get_jobs())
job_id = cron.get_jobs()[0].__getattribute__('id')
print(job_id)
print(type(cron.get_jobs()[0].__getattribute__('id')))


# slash command for changing time (hour) for tomorrow report
@app.route('/sat', methods=['POST'])
def hour_change():
    data = request.form  # 3- 5.55
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    print(text)

    if text == '':
        client.chat_postMessage(channel=channel_id, text='Nedostaje argument [hh]')
    elif metaweather.not_valid_text(text):
        client.chat_postMessage(channel=channel_id, text='Pazi kod unosa, argument mora biti znamenka od *0* do *23*')
    else:
        client.chat_postMessage(channel=channel_id,
                                text='*Slanje obavijesti o prognozi biti će svaki dan u ' + text + ' sati*')
        cron.reschedule_job(job_id, trigger='cron', hour=text, minute='0')
        print(cron.get_jobs())
        cron.print_jobs()

    return Response(), 200


atexit.register(lambda: cron.shutdown(wait=False))

if __name__ == "__main__":
    # ids = schedule_messages(SCHEDULED_MESSAGES)
    app.run()
