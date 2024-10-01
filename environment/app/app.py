from flask import Flask, request, jsonify, render_template
import os


app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    with open('./final hybrid.py', 'r') as file:
        script_code = file.read()
    exec(script_code, globals())
    return "done"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)