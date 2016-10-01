"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa
import random


def lambda_handler(request_obj, context=None):
    """
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    """

    metadata = {'user_name': 'Jennifer'}  # add your own metadata to the request using key value pairs

    ''' inject user relevant metadata into the request if you want to, here.
    e.g. Something like :
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}
    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''

    return alexa.route_request(request_obj, metadata)


@alexa.default
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request type """
    return alexa.respond('Just ask').with_card('Hello World')


@alexa.request("LaunchRequest")
def launch_request_handler(request):
    """ Handler for LaunchRequest """
    start_greeting = ('How YOUUU duuin brah? This is Marsala, your eventbrite asssistant coming to you live from the inside of the cylindrical container. Hit me with it.',
                      "Greetings earthlings. This is Mar-Sala. An advanced form of intelligence, the brain child of mixing Star Trek and Star Worlds. Please specify the parameters of your query",
                      "Hi guys. Tnis is Marsala. I'm your girl for parsing through Eventbrite. Tell me about what you're looking for.")
    return alexa.create_response(message=random.choice(start_greeting))


@alexa.request("SessionEndedRequest")
def session_ended_request_handler(request):
    end_greeting = ('Goodbye!', 'Ciao!', 'Adios amigos!', 'Sayonara!', 'Au revoir!', 'TTFN Ta-TA for now!')

    return alexa.create_response(message=random.choice(end_greeting))


@alexa.intent_handler('GiveMeTheInfo')
def get_event_info_handler(request):
    """
    This is the handler that for getting the event information of the request

    :param request:
    :return:
    """
    date_range = request.slots['DATE1']
    event_keyword = request.slots['Keyword']
    location = request.slots['Location']

    """
    TODO: Use the params to make Evenbrite API request and get the json response
    """

    # FIXME: change the output parameter to API results
    event_name = "Test Event"
    event_description = "Test Description"
    event_url = "https://www.eventbrite.com/"
    event_time = "10/1/2016 7PM"
    event_location = "Knoxville, Tennessee"

    large_image_url = "http://www.underconsideration.com/brandnew/archives/eventbrite_monogram.jpg"
    small_image_url = ""

    card = alexa.create_card(title=event_name, content=event_description, card_type='Standard')
    card['image'] = {"smallImageUrl": small_image_url,
                     "largeImageUrl": large_image_url}

    speech_message = "Looks like this fits the bill. There's a event called {} at {} at {}"\
        .format(event_name, event_location, event_time)

    return alexa.create_response(message=speech_message, card_obj=card)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--serve', '-s', action='store_true', default=False)
    args = parser.parse_args()

    if args.serve:
        ###
        # This will only be run if you try to run the server in local mode
        ##
        print('Serving ASK functionality locally.')
        import flask

        server = flask.Flask(__name__)


        @server.route('/')
        def alexa_skills_kit_requests():
            request_obj = flask.request.get_json()
            return lambda_handler(request_obj)


        server.run()