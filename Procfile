web: gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 alternatorparts.wsgi:application
migrate: python3 -m manage migrate && python3 -m manage collectstatic --noinput --clear
createuser: python3 -m manage createsuperuser --username admin --email admin@alternatorparts.com --noinput
makemigrations: python3 -m manage makemigrations --noinput
