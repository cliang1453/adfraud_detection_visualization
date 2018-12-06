from flask import Flask, request, json, render_template
import pickle
app = Flask(__name__)
@app.route('/')
def hello():
        return render_template('client_interface.html')

@app.route('/predict',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        model = pickle.load(open("model/model_xgboost.pickle", 'rb'))
        print(request.form)
        attribute = []
        #convert string to int
        attribute.append(int(request.form['ip']))
        attribute.append(int(request.form['app']))
        attribute.append(int(request.form['os']))
        attribute.append(int(request.form['device']))
        attribute.append(int(request.form['channel']))
        attribute.append(int(request.form['clicktime']))
        predict = model.predict(attribute)
        return render_template("client_interface.html", label = predict, post = True)

@app.route('/statistics')
def show():
    return render_template('interactive_visualization.html')

if __name__ == "__main__":
    app.run()
