from api_code import available_hours, appointment, open_hours, pricing
from flask import Flask, request, make_response, jsonify
import pprint

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

def results():
    
    req = request.get_json(force=True)
    response = {}

    
    query = req.get('queryResult')
    action = query['action']
    parameters = query['parameters']
    if action == "open_hours":
        date = parameters['date']
        print(date)
        response["fulfillmentText"] = open_hours(date)
    elif action == 'appointment':
        service = parameters['service']
        date = parameters['date']
        time = parameters['time']
        response["fulfillmentText"] = appointment(service, date, time)
    elif action == 'pricing':
        service = parameters['service']
        response["fulfillmentText"] = pricing(service)
    elif action == 'available_hours':
        service = parameters['service']
        date = parameters['date']
        response["fulfillmentText"] = available_hours(service, date)
    return response


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))


if __name__ == '__main__':
   app.run()

