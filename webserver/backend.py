from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/search')
def search():
    inp = str(request.args.get('s'))

    return return_info("yeet")

def return_info(stock):
    return stock + " still in progress"

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)
