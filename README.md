# MaxPorto

Personal portfolio website for Maximus Quinn Hertada, built with Django,
semantic HTML, and CSS 

## Features

- Responsive dark navy and electric-blue visual system.
- Sticky anchor navigation for Experience, Education, Project, Achievements,
  and Contact.
- English (`/`) and Indonesian (`/id/`) versions served by Django.
- Project, achievement, and contact sections.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/` for English or `http://127.0.0.1:8000/id/`
for Indonesian.



See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and
[docs/AI_DISCLOSURE.md](docs/AI_DISCLOSURE.md) for design and authorship notes.
