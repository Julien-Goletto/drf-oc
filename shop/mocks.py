import requests
from rest_framework import status

ECOSCORE_GRADE = 'd'

def mock_openfoodfact_success(self, method, url):
    def monkey_json():
        return {
            'product': {
                'ecoscore_grade': ECOSCORE_GRADE,
            }
        }
    
    response = requests.Response()
    response.status_code = status.HTTP_200_OK
    response.json = monkey_json
    return response