python manage.py tree_schema
if [ "$#" -eq 1 ]; then
	python manage.py upload_budget --clean --muni $1
	python manage.py muni2tree --clean --muni $1
fi

if [ "$#" -eq 2 ]; then
	python manage.py upload_budget --clean --muni $1 --year $2
	python manage.py muni2tree --clean --muni $1 --year  $2
fi
