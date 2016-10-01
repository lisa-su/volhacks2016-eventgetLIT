import requests
import datetime
import pprint
import calendar
import json


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
    def format_date(date, type="start"):
        if len(date) == 10 and ("W" not in date):
            if type == "start":
                return date + "T00:00:01"
            else:
                return date + "T23:59:59"
        elif len(date) == 7 and ("W" not in date):
            if type == "start":
                return date + "-01T00:00:01"
            else:
                return date + "-" + str(calendar.monthrange(int(date[:4]), int(date[5:]))[1]) + "T23:59:59"
        elif len(date) == 4 and ("X" not in date):
            if type == "start":
                return date + "-01-01T00:00:01"
            else:
                return date + "-12-31T23:59:59"
        elif len(date) == 4:
            if type == "start":
                return date[:-1] + "0-01-01T00:00:01"
            else:
                return date[:-1] + "9-12-31T23:59:59"
        elif len(date) in (7, 8) and ("W" in date) and ("WI" not in date):
            if type == "start":
                date_time = datetime.datetime.strptime(date + ' SUN', "%Y-W%U %a")
                return str(date_time)[:10] + "T00:00:01"
            else:
                date_time = datetime.datetime.strptime(date + ' SAT', "%Y-W%U %a")
                return str(date_time)[:10] + "T23:59:59"
        elif len(date) >= 10:
            if type == "start":
                date_time = datetime.datetime.strptime(date[:-3] + ' SAT', "%Y-W%U %a")
                return str(date_time)[:10] + "T00:00:01"
            else:
                date_time = datetime.datetime.strptime(date[:6] + str(int(date[6:-3]) + 1) + ' SUN', "%Y-W%U %a")
                return str(date_time)[:10] + "T23:59:59"
        else:
            return None

    def get_events(self, location, date=None, keywords=None):

        response_url = self.get_url() + "?token=" + self.get_token()

        # Filtering by address
        response_url += "&location.address=" + location

        if date is None:
            start = datetime.datetime.today().strftime('%Y-%m-%d') + "T00:00:01"
            end = datetime.datetime.today().strftime('%Y-%m-%d') + "T23:59:59"
            response_url += "&start_date.range_start=" + start + "&start_date.range_end=" + end
        else:
            start_date = self.format_date(date, "start")
            end_date = self.format_date(date, "end")
            if start_date is None:
                start = datetime.datetime.today().strftime('%Y-%m-%d') + "T00:00:01"
                end = datetime.datetime.today().strftime('%Y-%m-%d') + "T23:59:59"
                response_url += "&start_date.range_start=" + start + "&start_date.range_end=" + end
            else:
                response_url += "&start_date.range_start=" + start_date + "&start_date.range_end=" + end_date

        if keywords is not None:
            response_url += "&q=" + keywords

        print response_url

        print "before event"
        response = requests.get(response_url)
        print "after event"

        if 'events' in response.json().keys():
            if len(response.json()["events"]) > 3:
                data_dict = response.json()["events"][:3]
            else:
                data_dict = response.json()["events"]
        else:
            self.set_data({})
            return self.get_data()

        your_keys = ['name', 'description', 'url', 'start', 'end', 'venue_id', 'logo']
        new_dict = []
        count = 0
        for e in data_dict:
            new_dict.append({})
            for k in your_keys:
                if k == "url":

                    google_url = "https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyCixNDku0flyN9PFJT8Y-pjE8yg9bfnErk"
                    headers = {'content-type': 'application/json'}
                    data = {
                        "longUrl": e[k]
                    }
                    print "before url short"
                    url_shortener = requests.post(google_url, json.dumps(data), headers=headers)
                    print "after url short"
                    new_dict[count][k] = url_shortener.json()['id']

                elif k == 'venue_id':
                    temp_url = self.get_venue_url() + e[k] + "/" + "?token=" + self.get_token()
                    print "before venue"
                    venue = requests.get(temp_url)
                    print "after venue"

                    new_dict[count]['location'] = venue.json()['name']
                    new_dict[count]['location_address'] = venue.json()['address']['localized_address_display']
                elif k == "logo" and e[k] is not None:
                    new_dict[count]['small_image'] = e[k]['url']
                    new_dict[count]['large_image'] = e[k]['original']['url']
                elif isinstance(e[k], basestring):
                    new_dict[count][k] = e[k]
                else:
                    if e[k] is not None and 'text' in e[k].keys():
                        new_dict[count][k] = e[k]['text']
                    elif e[k] is not None and 'local' in e[k].keys():
                        new_dict[count][k] = e[k]['local']

            count += 1

        self.set_data(new_dict)

        return self.get_data()

a = PartyParrot()
pprint.pprint(a.get_events("Knoxville", "2016-10-01"))

