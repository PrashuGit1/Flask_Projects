# app.py
from flask import Flask, render_template, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError
from scraper import scrape_jobs
import pandas as pd
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev"  # for flash messages
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    company = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    salary = db.Column(db.String(120))
    skills = db.Column(db.String(500))
    link = db.Column(db.String(500))
    __table_args__ = (
        UniqueConstraint("title", "company", "location", name="uq_job_triplet"),
    )

@app.route("/")
def index():
    jobs = Job.query.order_by(Job.company.asc()).all()
    return render_template("index.html", jobs=jobs)

@app.route("/scrape")
def do_scrape():
    data = scrape_jobs()
    added, skipped = 0, 0
    for j in data:
        job = Job(
            title=j["title"],
            company=j["company"],
            location=j["location"],
            salary=j["salary"],
            skills=j["skills"],
            link=j["link"],
        )
        db.session.add(job)
        try:
            db.session.commit()
            added += 1
        except IntegrityError:
            db.session.rollback()
            skipped += 1
    flash(f"Scrape complete. Added {added}, skipped {skipped} duplicates.")
    return redirect(url_for("index"))

@app.route("/export.csv")
def export_csv():
    rows = Job.query.all()
    if not rows:
        flash("No data to export. Click 'Scrape now' first.")
        return redirect(url_for("index"))
    df = pd.DataFrame([{
        "title": r.title,
        "company": r.company,
        "location": r.location,
        "salary": r.salary,
        "skills": r.skills,
        "link": r.link,
    } for r in rows])
    path = os.path.join(os.getcwd(), "jobs_export.csv")
    df.to_csv(path, index=False)
    return send_file(path, as_attachment=True, download_name="jobs_export.csv")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
