# eventgetLIT
Volhacks @ UT Knoxville 

Authors: @miadantas @jboudreau3 @Yihsuan

eventgetLIT is a Amazon Alexa Skill Kit that integrates with the Eventbrite API using Python 2.7 to search for events. This program parses users' natural speech and serves keywords to the  API which in turn surfaces the most relevant events. This application was developed 9/30/16 - 10/2/16 as part of the University of Tennessee Knoxville's inaugural Volhacks Hackathon. 


#Basic Usage 
This project was this group's first attempt at programming hardware, and as such, the application we have built is based in simplicity. However, we have tried to create a comprehensive program that covers many variations of natural speech. Using Amazon Echo's native intent schema, utterance patterns, and lambda functions, Alexa is able to understand and parse almost 200 difference variances of asking for events including parameters such as _KEYWORDS_, _LOCATION_, and _DATE_. (Please refer to the _speechAssets_ folder for a complete summary of what Alexa can and cannot parse). Additionally, after taking these parameters and relaying information regarding events verbally, this program will surface a CARD directly to your Alexa app with the key event information and a shortened URL you may paste into a browser. 


#Easter Eggs
If you integrate this directly into your own Amazon Echo, try some of these phrases: 

>"What's going on today around the University of Georgia?"

>"What's going on today around the University of Tennessee?" (Try this one out a couple times) 

>"I'm done" 

**SEC fans be weary of asking what's going on in Orange Nation**

#Resources
* All code is in Python 2.7
    * Piped *requests* package 
* Amazon Echo's documentation online. This is a good start:  
    * https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/using-the-alexa-skills-kit-samples
* Eventbrite API
    * https://developer.eventbrite.com/
* Google URL Shortener API
    * https://developers.google.com/url-shortener/
* Please refer to the _speechAssets_ folder for a complete breakdown of the logic Alexa recognizes to parse speech.
  All aspects are customizable to fit your own speech patterns or whoever may use the app. If you have not programmed a skill
  before with Alexa, we **HIGHLY, HIGHLY** recommend you first refer to the Amazon Echo's documentation online. 

