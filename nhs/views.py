from django.shortcuts import render
import requests

# Create your views here.
def index(request):

    api_endpoint = 'https://sandbox.api.service.nhs.uk/hello-world/hello/world'

    try:
        # make get request to api endpoint
        response = requests.get(api_endpoint)

        # raise http error code if status is 4xx or 5xx
        response.raise_for_status()

        # reaching here means request was successful
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")

        content = {
            'data': response.text
        }

        return render(request, 'nhs/index.html', content)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None


    return render(request, 'nhs/index.html')