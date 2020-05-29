from flask import Flask, render_template, request, redirect, url_for
import csv
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():

    states = pd.read_csv('predictions.csv', nrows=0)
    state_name = []
    # print(states)

    for row in states:
        if row == "Unnamed: 0":
            continue
        row = row.replace('state_', "")
        state_name.append(row)

    return render_template("index.html", state_name=state_name)


if __name__ == "__main__":
    app.run()
