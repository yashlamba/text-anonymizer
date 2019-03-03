from flask import Flask, render_template, request, url_for
from Anonymizing_script import Anonymize

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST': 
        text = request.form['name']
        anonText = Anonymize(text)  
        return render_template('Anonymized.html', anonText = anonText, text = text) 
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)