python manage.py makemigrations users --noinput
python manage.py makemigrations chat --noinput
python manage.py makemigrations home --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
