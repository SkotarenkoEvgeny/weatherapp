import logging

from bs4 import BeautifulSoup

from weatherapp.core.abstract import Cache_controller
from weatherapp.core.abstract import WeatherProvider as Weather_settings


class RP5Provider(Weather_settings):
    call = 0

    def __init__(self):
        # (search_url, place, current_location)
        RP5Provider.call += 1
        logging.debug('init rp5', RP5Provider.call)
        self.site_name = 'rp5.ua'
        super().__init__(self.site_name)
        self.site_data = Weather_settings.read_settings(self)

    def parser(self):
        '''
        :return: site_name, temperature, place, cond from rp5
        '''
        body = body = self.bs_body_processor()
        temprege = body.find('span', 't_0').text
        place = body.find('div', {'id': 'pointNavi'}).text
        cond = body.find(id='forecastShort-content').find(class_='second-part') \
                   .previous.lstrip(' ')[:-2]
        return (self.site_name, temprege, place, cond)

    def links_search(url):

        raw_data = Cache_controller(url).cache_chose()
        body = BeautifulSoup(raw_data, "html.parser").find(class_='countryMap')
        if body != None:
            raw_data = body.findAll(class_='country_map_links')
            data = {}
            if raw_data != []:
                for i in raw_data:
                    data[i.b.text[:-1]] = 'http://rp5.ua' + i.b.a['href']
            else:
                raw_data = body.findAll(class_='href20')
                for i in raw_data:
                    data[i.text] = 'http://rp5.ua/' + i['href']
            return data
        else:
            return {}

    def temperature_per_hour(self):
        '''
        Data from rp5.com
        :return: list[site_name, mit temperature, max temperature,
        average temperature]
        '''
        pass
