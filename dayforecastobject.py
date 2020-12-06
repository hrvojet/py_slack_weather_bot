from metaweather import weather_state_abr, day_of_week
from datetime import date


class DayForecast:
    def __init__(self, map_):
        self.__weather_state_abbr = map_.get('weather_state_abbr')
        self.__applicable_date = map_.get('applicable_date')
        self.__min_temp = map_.get('min_temp')
        self.__max_temp = map_.get('max_temp')
        self.__the_temp = map_.get('the_temp')
        self.__wind_speed = map_.get('wind_speed')
        self.__air_pressure = map_.get('air_pressure')
        self.__humidity = map_.get('humidity')

    def get_day_of_week(self):
        return day_of_week.get(date.fromisoformat(self.__applicable_date).weekday())

    def get_weather_data(self):
        return {
            'wea_abbr': self.__weather_state_abbr,
            'wea_name': str(weather_state_abr.get(self.__weather_state_abbr)),
            'appl_date': self.__applicable_date,
            'the_temp': str(int(self.__the_temp)),
            'min_temp': str(int(self.__min_temp)),
            'max_temp': str(int(self.__max_temp)),
            'humidity': str(self.__humidity),
            'air_pres': str(self.__air_pressure),
            'day_of_w': self.get_day_of_week(),
            'wind_speed': str(int(self.__wind_speed * 1.61))  # mph to km/h
        }


class CityForecast:
    def __init__(self, api):
        self.__day_forecast_list = []
        for day in api.get('consolidated_weather'):
            self.__day_forecast_list.append(DayForecast(day))

        self.__title = api.get('title')
        self.__location_type = api.get('location_type')
        self.__woeid = api.get('woeid')

    def get_weather(self):
        dl = []
        for list_data in self.__day_forecast_list[1:]:
            dl.append(list_data.get_weather_data())

        return dl

    def get_weather_tomorrow(self):
        return self.__day_forecast_list[1].get_weather_data()

    def get_title(self):
        return self.__title

    def get_woeid(self):
        return self.__woeid


class BlockBuilder:
    def __init__(self, forecast, channel):
        self.__forecast = forecast
        self.__channel = channel

    def tomorrow_report(self):
        start_text = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": self.__forecast.get_title(),
                "emoji": True
            }
        }
        divider = {'type': 'divider'}

        weather_data = self.__forecast.get_weather_tomorrow()
        the_temp = int(weather_data.get('the_temp'))
        wind_spd = int(weather_data.get('wind_speed'))
        wea_abbr = weather_data.get('wea_abbr')
        weather_icon = 'https://www.metaweather.com/static/img/weather/png/' + wea_abbr + '.png'

        precipitation = ""
        if wea_abbr in ['sn', 'sl', 'h', 'hr', 'lr', 's']:
            precipitation = "Očekuju se oborine, nemoj zaboraviti *kišobran* :umbrella_with_rain_drops: "

        wind = ""
        if wind_spd >= 11:
            wind = "Puhat će "
            if 11 <= wind_spd <= 15:
                wind = wind + "lagani"
            elif 16 <= wind_spd <= 19:
                wind = wind + "osjetni"
            elif 20 <= wind_spd:
                wind = wind + "jak"

            wind = wind + " vjetar. "

        temp = ""
        if the_temp < 0:
            temp = "Sutra će temperatura biti u minusu jako se toplo obuci :snowflake: "
        elif 0 <= the_temp <= 10:
            temp = "Sutra će biti hladno, pa se zato toplo se obuci :scarf::coat: "
        elif 11 <= the_temp <= 20:
            temp = "Sutra se očekuju udobne tempreature, sukladno tome se odjeni :mostly_sunny: "
        elif 21 <= the_temp <= 25:
            temp = "Sutra se očekuje da će biti toplo, lagano se odjeni :sunny: "
        else:
            temp = "Sutra će biti vruče, razmisli o kratkim hlačama :thermometer: "

        final_str = temp + precipitation + wind

        return {
            "channel": self.__channel,
            "text": final_str
        }

    def get_week_forecast(self):
        start_text = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": self.__forecast.get_title(),
                "emoji": True
            }
        }
        divider = {'type': 'divider'}
        blocks = [start_text, divider]
        forecast_list = self.__forecast.get_weather()
        for weather_data in forecast_list:
            day = weather_data.get('day_of_w')
            the_temp = weather_data.get('the_temp')
            wea_abbr = weather_data.get('wea_abbr')
            wea_name = weather_data.get('wea_name')
            humidity = weather_data.get('humidity')
            air_pres = weather_data.get('air_pres')
            weather_icon = 'https://www.metaweather.com/static/img/weather/png/' + wea_abbr + '.png'
            text = day + "\n" + the_temp + "°C, " + wea_name + "\nVlažnost: *" + humidity + "%*\nTlak zraka: *" + air_pres + "*"
            tmp_section = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                },
                "accessory": {
                    "type": "image",
                    "image_url": weather_icon,
                    "alt_text": "computer thumbnail"
                }
            }
            blocks.append(tmp_section)
            blocks.append(divider)

        return {
            "channel": self.__channel,
            "blocks": blocks
        }

    def get_tomorrow_forecast(self):
        title = self.__forecast.get_title()
        weather_data = self.__forecast.get_weather_tomorrow()
        appl_date = weather_data.get('appl_date')
        the_temp = weather_data.get('the_temp')
        min_temp = weather_data.get('min_temp')
        max_temp = weather_data.get('max_temp')
        humidity = weather_data.get('humidity')
        air_pres = weather_data.get('air_pres')
        wea_abbr = weather_data.get('wea_abbr')
        wea_name = weather_data.get('wea_name')
        weather_icon = 'https://www.metaweather.com/static/img/weather/png/' + wea_abbr + '.png'
        text = 'Vrijeme sutra:\t*' + title + '\t' + the_temp + '°C*\n' + wea_name + ', od ' + min_temp + ' do ' + max_temp + '°C\nVlažnost: ' + humidity + '%\nTlak zraka: ' + air_pres
        return {
            "channel": self.__channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": weather_icon,
                        "alt_text": "computer thumbnail"
                    }
                }
            ]
        }
