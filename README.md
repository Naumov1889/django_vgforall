# django_vgforall
To run:
1. Create virtualenv: <code>virtualenv env</code>
2. Activate virtualenv: <code>source env/Scripts/activate</code> or <code>env\Scripts\activate</code>(Windows) or <code>source env/bin/activate</code>(Linux)
3. Install dependencies: <code>pip install -r requirements.txt</code>
4. Create database: <code>python manage.py makemigrations</code> and <code>python manage.py migrate</code>
5. Go to <code>.env.example</code>. Remove '.example' from the name of the file and fill the variables.
