from app import create_app
from rest_api.api import create_api


application = create_app()
create_api(application)

if __name__ == '__main__':
    application.run(host='localhost', debug=True, port=5000, threaded=True)
