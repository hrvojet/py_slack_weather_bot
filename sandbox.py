import metaweather

api_ = {
    "consolidated_weather": [
        {
            "id": 5724688828334080,
            "weather_state_name": "Heavy Cloud",
            "weather_state_abbr": "hc",
            "wind_direction_compass": "WSW",
            "created": "2020-12-04T19:22:49.742408Z",
            "applicable_date": "2020-12-04",
            "min_temp": -2.295,
            "max_temp": 2.88,
            "the_temp": 1.01,
            "wind_speed": 1.4451984512632892,
            "wind_direction": 240.86493783798147,
            "air_pressure": 1005.5,
            "humidity": 91,
            "visibility": 6.80090769903762,
            "predictability": 71
        },
        {
            "id": 6485682240356352,
            "weather_state_name": "Heavy Cloud",
            "weather_state_abbr": "hc",
            "wind_direction_compass": "ENE",
            "created": "2020-12-04T19:22:52.757646Z",
            "applicable_date": "2020-12-05",
            "min_temp": 1.4549999999999998,
            "max_temp": 8.58,
            "the_temp": 5.865,
            "wind_speed": 1.8423755035737956,
            "wind_direction": 57.73970724873155,
            "air_pressure": 1007.0,
            "humidity": 90,
            "visibility": 4.991164101646385,
            "predictability": 71
        },
        {
            "id": 6172004974592000,
            "weather_state_name": "Light Rain",
            "weather_state_abbr": "lr",
            "wind_direction_compass": "ENE",
            "created": "2020-12-04T19:22:55.654192Z",
            "applicable_date": "2020-12-06",
            "min_temp": 5.615,
            "max_temp": 11.33,
            "the_temp": 8.895,
            "wind_speed": 4.0312512700866945,
            "wind_direction": 65.84017171341453,
            "air_pressure": 1005.5,
            "humidity": 84,
            "visibility": 12.833489918873777,
            "predictability": 75
        },
        {
            "id": 5309918736285696,
            "weather_state_name": "Showers",
            "weather_state_abbr": "s",
            "wind_direction_compass": "SSW",
            "created": "2020-12-04T19:22:58.940580Z",
            "applicable_date": "2020-12-07",
            "min_temp": 5.0600000000000005,
            "max_temp": 10.594999999999999,
            "the_temp": 8.94,
            "wind_speed": 2.239053932779236,
            "wind_direction": 211.2161195898631,
            "air_pressure": 1004.5,
            "humidity": 83,
            "visibility": 13.155981567644954,
            "predictability": 73
        },
        {
            "id": 6163195828895744,
            "weather_state_name": "Light Rain",
            "weather_state_abbr": "lr",
            "wind_direction_compass": "NE",
            "created": "2020-12-04T19:23:02.446623Z",
            "applicable_date": "2020-12-08",
            "min_temp": 3.8099999999999996,
            "max_temp": 7.1850000000000005,
            "the_temp": 6.140000000000001,
            "wind_speed": 3.548802040173388,
            "wind_direction": 53.00489325099099,
            "air_pressure": 1005.5,
            "humidity": 90,
            "visibility": 10.598728425992206,
            "predictability": 75
        },
        {
            "id": 5327704430739456,
            "weather_state_name": "Heavy Rain",
            "weather_state_abbr": "hr",
            "wind_direction_compass": "N",
            "created": "2020-12-04T19:23:05.739365Z",
            "applicable_date": "2020-12-09",
            "min_temp": 2.9299999999999997,
            "max_temp": 7.105,
            "the_temp": 4.78,
            "wind_speed": 3.3060747236140937,
            "wind_direction": 0.9999999999999934,
            "air_pressure": 1007.0,
            "humidity": 85,
            "visibility": 9.305654974946313,
            "predictability": 77
        }
    ],
    "time": "2020-12-04T23:18:15.406268+01:00",
    "sun_rise": "2020-12-04T07:20:33.584304+01:00",
    "sun_set": "2020-12-04T16:12:10.885988+01:00",
    "timezone_name": "LMT",
    "parent": {
        "title": "Croatia",
        "location_type": "Country",
        "woeid": 23424843,
        "latt_long": "44.746712,15.340800"
    },
    "sources": [
        {
            "title": "BBC",
            "slug": "bbc",
            "url": "http://www.bbc.co.uk/weather/",
            "crawl_rate": 360
        },
        {
            "title": "Forecast.io",
            "slug": "forecast-io",
            "url": "http://forecast.io/",
            "crawl_rate": 480
        },
        {
            "title": "HAMweather",
            "slug": "hamweather",
            "url": "http://www.hamweather.com/",
            "crawl_rate": 360
        },
        {
            "title": "Met Office",
            "slug": "met-office",
            "url": "http://www.metoffice.gov.uk/",
            "crawl_rate": 180
        },
        {
            "title": "OpenWeatherMap",
            "slug": "openweathermap",
            "url": "http://openweathermap.org/",
            "crawl_rate": 360
        },
        {
            "title": "Weather Underground",
            "slug": "wunderground",
            "url": "https://www.wunderground.com/?apiref=fc30dc3cd224e19b",
            "crawl_rate": 720
        },
        {
            "title": "World Weather Online",
            "slug": "world-weather-online",
            "url": "http://www.worldweatheronline.com/",
            "crawl_rate": 360
        }
    ],
    "title": "Zagreb",
    "location_type": "City",
    "woeid": 851128,
    "latt_long": "45.807259,15.967600",
    "timezone": "Europe/Vienna"
}

# response = metaweather.get_tomorrow_forecast().json()

# print(api_obj.get_weather())
# bb_obj = BlockBuilder(api_obj, 'asd')
# block_day = bb_obj.get_tomorrow_forecast()
# block_week = bb_obj.get_week_forecast()
# print('end')
