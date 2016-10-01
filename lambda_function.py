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
        card_title, speech_output, speech_output, should_end_session
    ))


def get_welcome_response():
    session_attributes = {}
    card_title = "Party Parrot"
    welcome_options = ["Hello! Alexa here. Wanna tell me what type of events you're intersted in?",
                       "Hello! Alexa here. Wanna tell me what type of events you're intersted in?",
                       "Bored? Wanna branch out? Let's me hook you up with something fun to do!",
                       "Bored? Wanna branch out? Let's me hook you up with something fun to do!",
                       "Team Event-Get-LIT presents to you: Party Parrot, a game of event roulette"]
    speech_output = choice(welcome_options)
    reprompt_text = "I'm waiting..."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    session_attributes = {}
    speech_output = "You can aske me something like what's happening around Knoxville"
    reprompt_text = "I'm waiting..."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        "Help", speech_output, reprompt_text, should_end_session
    ))


def create_remain_result_attributes(remain_results):
    return {'remain_results': remain_results}


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
    else:
        this_event = result.pop(0)
        session_attributes = create_remain_result_attributes(result)
        result_msg = "Found the event {} on {} at {}.".format(this_event['name'],
                                                              this_event['start'][:10],
                                                              this_event['location'])

    return build_response(session_attributes, build_speechlet_response(
        card_title, result_msg, repromt_text, should_end_session))


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
    else:
        result_msg = "There's no result to show."

    return build_response(session_attributes, build_speechlet_response(
        card_title, result_msg, repromt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session, small_image=None, large_image=None):

    # TODO: make card item optional
    card = {
        "title": title,
        "content": output
    }

    if small_image is None and large_image is None:
        card['type'] = "Simple"
    else:
        card['type'] = "Standard"
        card["image"] = {}
        if small_image is None:
            card["image"]["largeImageUrl"] = large_image
        elif large_image is None:
            card["image"]["smallImageUrl"] = small_image
        else:
            card["image"]["largeImageUrl"] = large_image
            card["image"]["smallImageUrl"] = small_image

    response = {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": card,
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

    return response


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }