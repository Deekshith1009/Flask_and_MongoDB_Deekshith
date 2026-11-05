from flask import Flask,jsonify
import json
app =Flask(__name__)
@app.route('/')
def home():
    return 'Welcome to the Home Page'

@app.route('/api')
def get_users():
    with open("choco.json", "r") as f:
        data= json.load(f)
        return jsonify(data["users"])


if __name__ == '__main__':
    app.run(debug=True)
