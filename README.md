# Tracking-Melon
### ขั้นตอนการติดตั้ง

- python -m pip install django
- python -m pip install django-allauth
- python -m pip install mysqlclient
- python -m pip install django-mathfilters
- python -m pip install pythainlp

เพื่อติดตั้งหรือมีการเปลี่ยนแปลงฐานข้อมูล
- python manage.py makemigrations
- python manage.py migrate

ทำการรันโปรแกรม
- python manage.py runserver 127.0.0.1:8080

เพื่อสร้าง Admin 
- python manage.py createsuperuser