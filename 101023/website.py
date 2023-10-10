from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import requests
import os
import bar_graph
import line_graph
import flight_scraper
import natural_lang
import airline_review
import pandas as pda
from datetime import date



app = Flask(__name__, template_folder='templates')


location = {
      'BAH':"2024-03-02",
      'JED':"2024-03-09",
      "MEL":"2024-03-24",
      'TYO':"2023-04-07",
      'SHA':"2023-04-21",
      'MIA':"2023-05-05",
      'BLQ':"2023-05-19",
      "NCE":"2023-05-26",
      "YMQ":"2023-06-09",
      "BCN":"2023-06-23",
      "GRZ":"2023-06-30",
      "LHR":"2023-07-07",
      "BUD":"2023-07-21",
      "LGG":"2023-07-28",
      "AMS":"2023-08-25",
      "LIN":"2023-09-01",
      "BAK":"2023-09-15",
      "SIN":"2023-09-22",
      "AUS":"2023-10-20",
      "TLC":"2023-10-27",
      "SAO":"2023-11-03",
      "LAS":"2023-11-23",
      "DOH":"2023-12-01",
      "AUH":"2023-12-08"


}

@app.route("/")
def home():
    return render_template('homepage.html')


departure = "SIN"
destination = ""
dep_date = ""


@app.route("/", methods=(['GET', 'POST']))
def result():
    if request.method == 'POST':
        global departure
        global destination
        global dep_date

        destination = request.form.get("dest")
        # dep_date = request.form.get("date")

    dict = flight_scraper.initiateScrape(departure, request.form["dest"], location[request.form["dest"]])
    df = flight_scraper.excel(dict)
    line_graph.plot_linegraph(df)
    bar_graph.plot_bargraph(df)
    natural_lang.initiateNLP(dict)
    return render_template("display.html")


@app.route("/")
def linegraph():
    return render_template('line_graphtest.html')


@app.route("/")
def bargraph():
    return render_template('bar_graph.html')


@app.route("/")
def predictive():
    return render_template('predictive_analysis.html')


if __name__ == "__main__":
    app.run()
