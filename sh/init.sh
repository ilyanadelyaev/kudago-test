mkdir ./_logs

/usr/bin/env python ./manage.py makemigrations
/usr/bin/env python ./manage.py migrate
