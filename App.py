from flask import Flask, render_template, request, redirect, url_for
import csv
import pandas as pd
import Templates.bar_chart
from bokeh.embed import components


app = Flask(__name__)

@app.route("/")
def index():

    Templates.bar_chart.make_char()

    return(render_template("bar_chart.html"))


if __name__ == "__main__":
    app.run()
