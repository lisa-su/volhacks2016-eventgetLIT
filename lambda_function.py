import logging

from random import randint, choice

from datetime import date, datetime

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from index import PartyParrot


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_search():
    # TODO:
    msg = choice(["welcome_1", "welcome_2", "welcome_3"])
    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("GiveMeTheInfo")
def get_event_info(LOCATION, DATEE, KEYWORDZ):
    search_location = LOCATION
    search_date = DATEE
    search_keyword = KEYWORDZ

    if not search_location:
        search_location = "Knoxville"
    if not search_date:
        search_date = date.today().strftime('%Y-%m-%d')
    if not search_keyword:
        msg = render_template('no_keyword')
        return question(msg)

    search_msg = render_template('repeat', keyword=search_keyword, location=search_location,
                                 date=search_date)

    query = PartyParrot()
    result = query.get_events(search_location, search_date, search_keyword)
    if len(result) == 0:
        result_msg = render_template('empty')
    else:
        result = result[0]
        result_msg = render_template('result', name=result['name'], date=result['start'][:10],
                                           location=result['location'])

    #return statement(search_msg)
    return statement(result_msg)


if __name__ == '__main__':

    app.run(debug=True)