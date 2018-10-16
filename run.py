from app import application

if __name__ == '__main__':
    application.run(host='localhost', debug=True, port=5000, threaded=True)
