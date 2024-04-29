# routes.py

from app import app
from flask import jsonify, render_template, request
import requests

#getting the api key
apiKey = app.config['TIINGO_API_TOKEN']
async def get_tiingo_data(keyword):
    
    #print('api-key=',apiKey)

    #constructing the endpoint
    urlOne = 'https://api.tiingo.com/tiingo/daily/'
    urlOneTwo = 'https://api.tiingo.com/iex/'
    urlTwo = '?token='
    endpoint = ''.join([urlOne, keyword, urlTwo, apiKey])
    endpointTwo = ''.join([urlOneTwo, keyword, urlTwo, apiKey])

    #print('endpoint=',endpoint)
    #print('endpointTwo=',endpointTwo)

    try:
        # Making a HTTPS GET request to Tiingo endpoint
        response = requests.get(endpoint)
        responseTwo = requests.get(endpointTwo)
        
        # Checking if the request was successful (status code 200)
        if response.status_code == 200 & responseTwo.status_code == 200:
            # Returning the response from the API call
            # print('ressults=', response.json())
            return {'daily': response.json(), 'iex': responseTwo.json()}
        else:
            # If the request was not successful
            #print('ressults= API call failed')
            return {'error': 'API call failed', 'status':response.status_code}
    except Exception as e:
        # Handle any exceptions that occur during the API call
        return {'error': str(e), 'status': 500}

@app.route('/process_input/<input>', methods=['GET'])
async def process_input(input):
    # Checking if request contains JSON data
    if input: #request.is_json:
        # Getting JSON data from request
        #json_data = request.json
        #print('input_value', json_data)
        #input_value = json_data.get('input')

        if input is not None:
            request_value = await get_tiingo_data(input)
            #print('request_value', request_value)
            result = {'message': 'Input value received and processed successfully', 'data': request_value}

            # print('result' , result)
            # Returning a JSON response
            return jsonify(result), 200
        else:
            error = {'error': 'Input value not found in request'}
            return jsonify(error), 400
    
    else:
        # If request does not contain JSON data, an error is returned
        error = {'error': 'Request does not contain JSON data'}
        return jsonify(error), 400
    
@app.route('/')
def index():
    return render_template('index.html')