from run import model
from flask import Flask, request, json, render_template
app = Flask(__name__)
@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'GET':
        attribute = []
        #convert string to int
        attribute.append(int(request.form['ip']))
        attribute.append(int(request.form['app']))
        attribute.append(int(request.form['os']))
        attribute.append(int(request.form['device']))
        attribute.append(int(request.form['channel']))
        attribute.append(int(request.form['click_time']))
        predict_result = model.predict(attribute)
        return render_template("index.html", label = predict_result)