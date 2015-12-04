echo '==========================================='
echo "Initialize database"
echo '==========================================='
/usr/bin/env python ./manage.py makemigrations
/usr/bin/env python ./manage.py migrate

echo '==========================================='
echo "create ADMIN user for /admon page"
echo '==========================================='
/usr/bin/env python ./manage.py createsuperuser
