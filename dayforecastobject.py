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
            'day_of_w': self.get_day_of_week()
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
            print(type(day), type(the_temp), type(wea_name), type(wea_abbr), type(humidity), type(air_pres))
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
        print(weather_data.get('day_of_w'))
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