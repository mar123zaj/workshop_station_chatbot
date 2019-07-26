# Workshop station chatbot #

#### What is this? ####

This is simple chatbot done with Dialogflow and Python and Google Calendar API. Chatbot can be connected with Google Calendar. Backend is wrote in Python with Flask framework.

### Skills of workshop station chatbot: ###

* make an appointment for you
* send you few available hours in date wich you will give him
* inform you about pricing
* give you open hours for specific day or all days of week

#### What do I need to do to run this? ####

1. Sing-up to Dailogflow.
2. Make an agent.
3. Upload workshop_station_chatbot.zip
4. To run webhook you will need ngrok program, you can download it [here](https://ngrok.com/download).
5. Download Python 3 [here](https://www.python.org/downloads/).
6. Install requirements.txt([guide how to do this](https://stackoverflow.com/questions/7225900/how-to-install-packages-using-pip-according-to-the-requirements-txt-file-from-a)).
7. Run two command line interpreters, one for ngrok, and one for webhook.
8. In first one navigate to webhook_app.py and type `python3 webhook_app.py` or `python webhook_app.py`, you should see something like this:
![](https://i.imgur.com/PsKLewR.jpg)
9. In second one navigate to ngrok.exe and type `ngrok.exe http 5000`, you should see something like this:
![](https://i.imgur.com/xSDzofx.jpg)
10. Now you have working webhook and endpoint to communicate with our Dialogflow agent.
11. Go to Dialogflow and find Fulfillment section on left side of page and enable Webhook.
12. Copy link from ngrok.exe window(i.e. http://114d55b5.ngrok.io) and paste it into URL lable in Dialogflow Fulfillment. Remember to add "\webhook" at the end of the link. For example, my link would look like this: http://114d55b5.ngrok.io/webhook. Then save.
13. If you want to give your agent ability to be communicated with Google Calendar you will need to crate storage.json etc. For more info go to [guide for Google Calendar](https://developers.google.com/calendar/overview).
14. After this we can try our Dialogflow agent in test section on right side of Dialogflow page.
15. Have fun!
