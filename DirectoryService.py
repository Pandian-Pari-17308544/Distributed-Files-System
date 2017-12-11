from flask_api import FlaskAPI, status
from flask import request
import requests
import SecurityService as ss

app = FlaskAPI(__name__)


file_server_url = 'http://127.0.0.1:'


@app.route('/get_directory/<filename>', methods=['GET'])
def get_directory(filename):
    for n in [8007, 8008]:
        server_url = file_server_url + str(n) + "/find/" + filename
        in_directory = requests.get(server_url)
        status_code = in_directory.status_code
        if status_code == 200:
            return in_directory.json()
    return {'Error:': 'File does not exist amongst servers.'}


@app.route('/open', methods=['GET'])
def open_file():
    file = request.args.to_dict()
    for n in [8007, 8008]:
        server_url = file_server_url + str(n) + "/open?" + 'filename='+file['filename'] + '&userId='+file['userId']
        in_directory = requests.get(server_url)
        status_code = in_directory.status_code
        if status_code == 200:
            return in_directory.json()
        elif status_code == 409:
            return {'Error:': 'File is already locked.'}, status.HTTP_404_NOT_FOUND
    return {'Error:': 'File does not exist amongst servers.'}, status.HTTP_404_NOT_FOUND


@app.route('/write', methods=['POST'])
def write_file():
    file = request.json
    server_url = file_server_url + file['server_port'] + "/write"
    write = requests.post(server_url, json=file)
    status_code = write.status_code
    if status_code == 200:
        return "File successfully upated."
    return 'Error: Unknown Error.'


@app.route('/add', methods=['POST'])
def add_file():
    file = request.json
    for n in [8007, 8008]:
        server_name = requests.get(file_server_url + str(n) + "/name")
        if server_name.text == file['filepath']:
            post = requests.post(file_server_url + str(n) + "/add", json=file)
            return post.text
    return 'Error: No such server exists.'


if __name__=='__main__':
    app.run(port=8002)