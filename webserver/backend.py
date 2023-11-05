from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        data = request.json['key']

        return jsonify(data)



def return_info(stock):
    return stock + " still in progress"

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
