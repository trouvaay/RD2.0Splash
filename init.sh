#heroku pg:reset HEROKU_POSTGRESQL_PINK_URL --app appnam

# drop all db table
#./manage.py sqlclear app1 app2 app3 | ./manage.py dbshell

cd src

python manage.py syncdb
#python manage.py migrate
python manage.py flush
#python manage.py createsuperuser
#
python manage.py check_permissions
#
python manage.py loaddata ./fixtures/sites.json
#


cd ..