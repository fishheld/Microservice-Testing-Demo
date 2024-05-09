from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


@app.route('/')
def start():
    return "ui-service"


@app.route('/httptest')
def test():
    # 向微服务B发送请求
    response = requests.post('http://webapp2:5001/query', json={'input': 'Tom'})
    return f"success! result:{response.text}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)