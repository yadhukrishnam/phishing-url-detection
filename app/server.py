from flask import Flask, json, request, jsonify
from flask.helpers import make_response
from flask.templating import render_template
from sklearn.neighbors import KNeighborsClassifier
from parser import Parser
import pandas as pd
import numpy as np

df = pd.read_csv("./datasets/processed_final.csv")

arr = df.values
X = arr[:,0:30]
Y = arr[:,30]

knn_classifier = KNeighborsClassifier(n_neighbors=3)
knn_classifier.fit(X, Y.astype('int'))

app = Flask(__name__)

database = {}

@app.route("/", methods=["POST"])
def process_url():
    url = request.form["url"]
    features = Parser(url).parse()
    features.pop("url", None)
    features.pop("char_repeat", None)
    features.pop("abnormal_subdomain", None)

    vals = [features[x] for x in features]
    final_features = [np.array(vals)]

    prediction = knn_classifier.predict(final_features)
    if prediction[0] == 1:
        msg = f"The URL {url} appears to be phishing."
        database[url] = "P"
    else:
        msg = f"The URL {url} does not appear to be a phishing URL."
        database[url] = "S"

    return render_template("index.html", message=msg, recent=database)


@app.route('/', methods=['GET'])
def main():
    msg = "Please enter a URL"
    print (database)
    return render_template("index.html", message=msg, recent=database)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8889, debug=True) 