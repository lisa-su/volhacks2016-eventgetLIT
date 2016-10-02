from datetime import date
from query import PartyParrot
from random import choice

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.8f0d2afb-f869-4059-b16a-b2fb492acca6"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])


def on_session_started(session_started_request, session):
    print "Starting new session."


def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GiveMeTheInfo":
        return get_event_info(intent, session)
    elif intent_name == "GetNextIntent":
        return get_next_event(intent, session)
    elif intent_name == "VolHacksIntent":
        return get_volhack_response(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent. Intent_name: " + intent_name)


def on_session_ended(session_ended_request, session):
    print "Sayonara..."
    # Cleanup goes here...


def handle_session_end_request():
    session_attributes = {}
    card_title = "Party Parrot - Thanks"
    speech_output = "Thank you for using the Party Parrot"
    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, speech_output, should_end_session, False
    ))


def get_welcome_response():
    session_attributes = {}
    card_title = "Party Parrot"
    welcome_options = ["Hello! Alexa here. Wanna tell me what type of events you're interested in?",
                       "Hello! Alexa here. Wanna tell me what type of events you're interested in?",
                       "Bored? Wanna branch out? Let me hook you up with something fun to do!",
                       "Bored? Wanna branch out? Let me hook you up with something fun to do!",
                       "Team Event-Get-LIT presents to you: Party Parrot, a game of event roulette"]
    speech_output = choice(welcome_options)
    reprompt_text = "I'm waiting..."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, False))


def get_help_response():
    session_attributes = {}
    speech_output = """To use Party Parrot, tell me what type of event you'd be interested in attending
    with complete sentences, such as Find me events about food this week in Atlanta or Is there anything around
     San Francisco this weekend."""
    reprompt_text = "I'm waiting..."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        "Help", speech_output, reprompt_text, should_end_session, False
    ))


def create_remain_result_attributes(remain_results):
    return {'remain_results': remain_results}


def get_volhack_response(intent, session):
    session_attributes = {}
    card_title = None
    should_end_session = False
    repromt_text = "What else do you need?"

    volhacks_keyword = intent['slots']['VolHacks'].get('value')
    volhacks_response = ["""What's going on? Why, only Volhacks - the littest thing to happen on UT's campus.
    Except, well, when they crushed the Gators last week.""",
                         """"If you're looking for a great time, Volhacks is going on right now.
                         Only a scrub like a U-G-A grad would miss this.""",
                         """You're looking for plans today?
                         If you're not at Volhacks already you might as well be a Bama fan"""]
    if volhacks_keyword is not None and set(map(lambda x: x.lower(), volhacks_keyword.split(' '))).intersection(['ut', 'tennessee', 'knowxville', 'volhacks', 'volhack']):
        result_msg = choice(volhacks_response)
    elif volhacks_keyword is None:
        result_msg = "I don't understand what you said."
    else:
        result_msg = "Who really cares? You're in Big Orange Country now."

    return build_response(session_attributes, build_speechlet_response(
        card_title, result_msg, repromt_text, should_end_session))


def get_event_info(intent, session):
    session_attributes = {}
    card_title = "Event Info"
    should_end_session = False
    repromt_text = "What else do you need?"

    search_location = intent['slots']['LOCATION'].get('value')
    search_keyword = intent['slots']['KEYWORDZ'].get('value')
    search_date = intent['slots']['DATEE'].get('value')

    if not search_location:
        search_location = 'Knoxville'
    if not search_date:
        search_date = date.today().strftime('%Y-%m-%d')

    query = PartyParrot()
    result = query.get_events(search_location, search_date, search_keyword)

    if len(result) == 0:
        result_msg = "Sorry, no result. Please try again."

        return build_response(session_attributes, build_speechlet_response(
            card_title, result_msg, repromt_text, should_end_session, False))
    else:
        this_event = result.pop(0)
        if search_keyword is not None:
            repeat_msg = "I found events about {} around {} near the date {}.".format(search_keyword,
                                                                                      search_location,
                                                                                      this_event['start'][:10])
        else:
            repeat_msg = "I found events in {} around the date {}.".format(search_location,
                                                                           this_event['start'][:10])

        session_attributes = create_remain_result_attributes(result)
        result_msg = "The event is {} on {} at {}.".format(this_event['name'],
                                                           this_event['start'][:10],
                                                           this_event['location'])

        result_msg = repeat_msg + result_msg

        if 'small_image' in this_event.keys():
            sm = this_event['small_image']
        else:
            sm = None

        if 'large_image' in this_event.keys():
            lg = this_event['large_image']
        else:
            lg = None

        if 'url' in this_event.keys():
            u = this_event['url']
        else:
            u = None

        return build_response(session_attributes, build_speechlet_response(
            card_title, result_msg, repromt_text, should_end_session, True, sm, lg, u))


def get_next_event(intent, session):
    session_attributes = {}
    should_end_session = False
    card_title = "Event Info"
    repromt_text = "What else do you need?"

    if session.get('attributes', {}) and "remain_results" in session.get('attributes', {}) \
            and session['attributes']['remain_results']:
        remain_results = session['attributes']['remain_results']    # a list of remain results
        this_event = remain_results.pop(0)
        session_attributes = create_remain_result_attributes(remain_results)
        result_msg = "Found the event {} on {} at {}.".format(this_event['name'],
                                                              this_event['start'][:10],
                                                              this_event['location'])

        if 'small_image' in this_event.keys():
            sm = this_event['small_image']
        else:
            sm = None

        if 'large_image' in this_event.keys():
            lg = this_event['large_image']
        else:
            lg = None

        if 'url' in this_event.keys():
            u = this_event['url']
        else:
            u = None

        return build_response(session_attributes, build_speechlet_response(
            card_title, result_msg, repromt_text, should_end_session, True, sm, lg, u))
    else:
        result_msg = "There's no result to show."

        return build_response(session_attributes, build_speechlet_response(
            card_title, result_msg, repromt_text, should_end_session, False))


def build_speechlet_response(title, output, reprompt_text, should_end_session, show_card=False, small_image=None,
                             large_image=None, short_url=None):

    response = {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

    if show_card:
        if short_url is not None:
            output += "\n" + short_url

        card = {
            "title": title
        }

        if small_image is None and large_image is None:
            card['type'] = "Simple"
            card["content"] = output
        else:
            card['type'] = "Standard"
            card["text"] = output
            card["image"] = {}
            if small_image is None:
                card["image"]["largeImageUrl"] = large_image
            elif large_image is None:
                card["image"]["smallImageUrl"] = small_image
            else:
                card["image"]["largeImageUrl"] = large_image
                card["image"]["smallImageUrl"] = small_image

        response["card"] = card

    return response


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }

