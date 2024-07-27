## How to run locally

### Prerequisites
- Python 3.6 or higher find it [here](https://www.python.org/downloads/)
- pip package manager is required to install the dependencies
- venv package is required to create a virtual environment

Clone the repository
```bash
git clone repo_url
```
Create a virtual environment
### LINUX
```bash
python3 -m venv venv
source venv/bin/activate
```
### WINDOWS
```bash
python -m venv venv
venv\Scripts\activate
```
Install the dependencies, Migrations and run the server
```bash
pip install -r requirements.txt
python manage.py makemigrations core accounts services
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```# Cleaning-Services
# Cleaning-Services
# Cleaning-Services
# Cleaning-Services
# Cleaning-Services
