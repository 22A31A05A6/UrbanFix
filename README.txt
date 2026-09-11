URBAN MANAGEMENT SYSTEM

1. Create/activate a virtual environment.
2. Install dependencies:
   pip install -r requirements.txt
3. Run migrations:
   python manage.py migrate
4. Optional: create an admin/municipal officer:
   python manage.py createsuperuser
   The superuser is staff and can use /admin-dashboard/.
5. Run:
   python manage.py runserver

Main pages:
/                 Home
/register/        Citizen registration
/login/           Citizen login
/dashboard/       Citizen dashboard
/report/          Report an issue
/complaints/      My complaints
/admin/           Django admin
/admin-dashboard/ Municipal officer dashboard (staff users)

Uploaded images are stored under media/.
