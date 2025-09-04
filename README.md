# Lost People Finder

A Django web application that helps users report and search for missing people. The system allows authenticated users to add missing person entries, create reports, and perform advanced searches using multiple filters, including blood type and parental blood types.

---

## Features

- **User Authentication**: Signup, login, and logout functionality.
- **Add Missing Person**: Authenticated users can add missing persons and generate a report automatically.
- **Advanced Search**:
  - Search by name, disappearance location, date range.
  - Filter by blood type, parental blood types (with RH factor consideration).
- **Reports Management**: View and manage reports for missing persons.
- **API Endpoints**: Provides API access for searching missing persons with authentication.

---

## Project Structure

lost/
├── finder/ # Django app
│ ├── migrations/
│ ├── templates/finder/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── utils.py
│ ├── serializers.py
│ └── urls.py
├── lost/ # Django project folder
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── manage.py
└── README.md


---

## Setup Instructions

1. **Clone the repository**:

```bash
git clone //github.com/amlfarrag3/Lost.git
cd lost

## Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt

## Apply migrations:

python manage.py makemigrations
python manage.py migrate

## Create a superuser:
python manage.py createsuperuser

## Run the development server:
python manage.py runserver

## Open your browser at http://127.0.0.1:8000/.
```


## Usage

Go to Signup to create a new user.

Login to access the dashboard.

Use Add Missing Person to add entries.

Use Advanced Search to filter missing persons.

View reports under Reports.

## API Endpoints

    home =  http://127.0.0.1:8000/.
    GET /home/: Go to home page  (requires authentication).
    GET /advanced-search/: Search missing persons  (requires authentication).
    GET /reports/:Reports list  (requires authentication).
    POST /missing/add/: Add missing persons  (requires authentication).
    GET /login/: Login  
    GET /logout/: Logout 
    POST /signup/: Signup 
   

## Dependencies

Django

Django REST Framework

Pillow (for image uploads)

## Notes

Only authenticated users can add missing persons or create reports.

The system automatically creates a Searcher profile for each new user using signals.
