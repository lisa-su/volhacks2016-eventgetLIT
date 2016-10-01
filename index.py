import requests
import datetime
import pprint


class PartyParrot:
    def __init__(self):
        self.data = {}
        self.url = "https://www.eventbriteapi.com/v3/events/search/"
        self.venue_url = "https://www.eventbriteapi.com/v3/venues/"
        self.token = "JMZ7LLBPYVZL3NEUIF66"

    def get_url(self):
        return self.url

    def get_venue_url(self):
        return self.venue_url

    def get_token(self):
        return self.token

    def set_data(self, d):
        self.data = d

    def get_data(self):
        return self.data

    @staticmethod
    def format_date(date):
        if len(date) == 10 and ("W" not in date):
            return date + "T00:00:01"
        elif len(date) == 7 and ("W" not in date):
            return date + "-01T00:00:01"
        elif len(date) == 4 and ("X" not in date):
            return date + "-01-01T00:00:01"
        elif len(date) == 4:
            return date[:-1] + "0-01-01T00:00:01"
        elif len(date) in (7, 8) and ("W" in date) and ("WI" not in date):
            date_time = datetime.datetime.strptime(date + ' MON', "%Y-W%U %a")
            return str(date_time).replace(" ", "T")
        elif len(date) >= 10:
            date_time = datetime.datetime.strptime(date[:-3] + ' SAT', "%Y-W%U %a")
            return str(date_time).replace(" ", "T")
        else:
            return None

    def get_events(self, location, date=None, keywords=None):

        response_url = self.get_url() + "?token=" + self.get_token()

        # Filtering by address
        response_url += "&location.address=" + location

        if date is None:
            response_url += "&start_date.keyword=today"
        else:
            string_date = self.format_date(date)
            if string_date is None:
                response_url += "&start_date.keyword=today"
            else:
                response_url += "&start_date.range_start=" + string_date

        if keywords is not None:
            response_url += "&q=" + keywords

        print response_url

        response = requests.get(response_url)

        if 'events' in response.json().keys():
            data_dict = response.json()["events"][:2]

        your_keys = ['name', 'description', 'url', 'start', 'end', 'venue_id']
        new_dict = []
        count = 0
        for e in data_dict:
            new_dict.append({})
            for k in your_keys:
                if k == 'venue_id':
                    temp_url = self.get_venue_url() + e[k] + "/" + "?token=" + self.get_token()
                    venue = requests.get(temp_url)

                    new_dict[count]['location'] = venue.json()['name']
                    new_dict[count]['location_address'] = venue.json()['address']['localized_address_display']

                elif isinstance(e[k], basestring):
                    new_dict[count][k] = e[k]
                else:
                    if 'text' in e[k].keys():
                        new_dict[count][k] = e[k]['text']
                    elif 'local' in e[k].keys():
                        new_dict[count][k] = e[k]['local']

            count += 1

        self.set_data(new_dict)

        return self.get_data()

a = PartyParrot()
pprint.pprint(a.get_events("Atlanta", "2016-10-02"))

