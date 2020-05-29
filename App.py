from flask import Flask, render_template, request, redirect, url_for
import csv
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    states = []
    predictions = []
    with open('predictions.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for state in row: 
                    if state == '' or state == 'predicted_cases': 
                        continue
                    state = state.replace('state_', "")
                    states.append(state)
                line_count += 1
            else:
                predictions.append(row[-1])
                line_count += 1
    results = dict(zip(states, predictions))
    print(results)

    return render_template("index.html", results = results)


if __name__ == "__main__":
    app.run()
