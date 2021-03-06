Joshua Saiers
Belelvue University
5/15/20222

import zipcodes
import requests


def isAnswer(answer):
    """
    Test if an answer is in Y or N and return True or False
    """
    if answer.upper() in ('Y', 'N'):
        return True


def get_keyword():
    """
    Get search keywords either 5 digit zip code or city name from the user, validate, and return
    :return: Only validated keyword will return
    """
    while True:
        keyword = input('Please enter 5 digits Zip Code or City Name: ')
        if validate_keyword(keyword):  # validate the key and return True if pass the validation test
            return keyword
        else:
            # If not validated, send a warning to the user
            print('Invalid Zip Code or City Name!')
            continue


def validate_keyword(keyword):
    """
    Takes keyword either 5 digit zip code or city name, validate using zipcodes modules, and return the test result
    :param keyword: keyword 5 digit zip code or city name
    :return: True or False
    """
    if keyword.isnumeric() and len(keyword) == 5:
        test_result = zipcodes.matching(keyword)  # If matching, the length will be greater than 0, otherwise empty
        if test_result.__len__() > 0:
            return True  # if matching zip code, return True
        else:
            print('---------------------------------------------------')
            print("In valid Zip Code!")
            print('---------------------------------------------------')
            return False  # If no matching zip code, return False
    elif keyword.isnumeric() and len(keyword) != 5:
        print('---------------------------------------------------')
        print('Please enter 5 digits Zip Code!')  # If only numeric but not 5 digits, return False
        print('---------------------------------------------------')
        return False
    elif keyword.isalpha():  # If a string is entered without number, then it's city name
        test_result = zipcodes.filter_by(city=keyword)  # Test if a city exists
        if test_result.__len__() > 0:
            return True  # if matching city, return True
        else:
            print('---------------------------------------------------')
            print("In valid City Name!")
            print('---------------------------------------------------')
            return False  # If no matching city, return False
    else:
        # If a keyword is not either zip or city, then return False
        return False


class WeatherForecast(object):
    """
    Class will receive a key from the user, forecast the weather based on key value, and print the result.
    Fields:
        keyword: stores a valid user input, zip code or city name
        url: stores API address
        key: stores a private access key
        header: stores header configuration
        weather: stores weather forecast values from the server
    Methods:
        forecast_weather: request weather information from the server and stores the response in weather variable
        print_weather: print the weather in a readable format
    """

    def __init__(self):
        self.keyword = None
        self._url = 'https://api.openweathermap.org/data/2.5/weather'
        self._key = 'd8a620617540a1b64554015f7304d205'
        self._header = {'cache-control': 'no-cache'}
        self.weather = None

    def forecast_weather(self):
        """
        Builds a query based on the type of key value, request to the server, and receive the result
        :return: NONE
        """
        try:
            # If a key is a zip code
            if self.keyword.isnumeric():
                qry_weather = {'zip': self.keyword,
                               'APPID': self._key,
                               'units': 'imperial'}
            # If a key is a city name
            else:
                qry_weather = {'q': self.keyword,
                               'APPID': self._key,
                               'units': 'imperial'}
            # Send the request to the API and store the result in json format
            response_weather = requests.get(self._url, headers=self._header, params=qry_weather)
            self.weather = response_weather.json()
            print('---------------------------------------------------')
            print('Connection was successful!')
            print('---------------------------------------------------')
        except Exception:
            print('---------------------------------------------------')
            print('Unable to connect to the server, please try again!')
            print('---------------------------------------------------')

    def print_weather(self):
        """
        Parse and print weather information in a nice format.
        :return: NONE
        """
        name = self.weather['name']
        main_pressure = self.weather['main']['pressure']
        main_humidity = self.weather['main']['humidity']
        main_temp = self.weather['main']['temp']
        main_temp_min = self.weather['main']['temp_min']
        main_temp_max = self.weather['main']['temp_max']
        weather_desc = self.weather['weather'][0]['description']
        wind_deg = self.weather['wind']['deg']
        wind_speed = self.weather['wind']['speed']
        print('---------------------------------------------------')
        print('Hi, this is a weather forecast program')
        print('---------------------------------------------------')
        print('Here is the weather information in {}:'.format(name))
        print('The current pressure is {} and humidity is {}.'.format(main_pressure, main_humidity))
        print('The current temperature is {}, the highest is {}, and the lowest is {}.'.format(main_temp, main_temp_max, main_temp_min))
        print('The degree of wind is {} and the speed is {}.'.format(wind_deg, wind_speed))
        print('The bottom line is that the weather is {}.'.format(weather_desc))
        print('---------------------------------------------------')

def main():
    print('---------------------------------------------------')
    print('------------Welcome to Weather Forecast------------')
    print('---------------------------------------------------')
    while True:
        print('Do you want to display weather?')
        answer = input('Y for yes, N for quit the program: ')
        # If the answer is not in Y or N, then send a warning and continue
        if not isAnswer(answer):
            print('Only enter Y or N for your answer!')
            continue
        # If the answer is N, then quit the program
        elif answer.upper() == 'N':
            break
        else:
            weather_forecast = WeatherForecast()
            weather_forecast.keyword = get_keyword()
            weather_forecast.forecast_weather()
            weather_forecast.print_weather()


if __name__ == '__main__':
    main()
