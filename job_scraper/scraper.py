# scraper.py
import requests
from bs4 import BeautifulSoup

FAKE_JOBS_URL = "https://realpython.github.io/fake-jobs/"

def scrape_jobs():
    """Returns list of dicts: title, company, location, salary, skills, link."""
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(FAKE_JOBS_URL, headers=headers, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    cards = soup.select("div.card-content")

    jobs = []
    for c in cards:
        title = c.select_one("h2.title").get_text(strip=True)
        company = c.select_one("h3.subtitle").get_text(strip=True)
        location = c.select_one("p.location").get_text(strip=True)
        # The fake site doesn’t have salary/skills; we’ll fill graceful defaults.
        salary = "Not disclosed"
        description = " ".join([p.get_text(" ", strip=True) for p in c.select("div.content p")])
        # naive keyword scan for demo
        keywords = ["Python","Django","Flask","SQL","AWS","Docker","Kubernetes","Java","JavaScript"]
        skills = ", ".join([k for k in keywords if k.lower() in description.lower()]) or "N/A"
        link = c.find("a", string="Apply")["href"] if c.find("a", string="Apply") else None

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "skills": skills,
            "link": link,
        })
    return jobs
