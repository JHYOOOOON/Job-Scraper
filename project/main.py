from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file
import datetime

app = Flask("WebScrapper")

db = {}

year = datetime.datetime.now().year


@app.route("/")
def home():
    return render_template("home.html", year=year)


@app.route("/report")
def report():
    word = request.args.get("word")
    existingJobs = db.get(word)
    if word:
        word = word.lower()
        jobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
    else:
        return redirect("/")

    if jobs:
        return render_template("report.html", searchingBy=word,
                               resultsNumber=len(jobs), jobs=jobs, year=year)
    else:
        return render_template("error.html", searchingBy=word, year=year)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv", as_attachment=True)
    except:
        return redirect("/")


app.run(host="127.0.0.1")
