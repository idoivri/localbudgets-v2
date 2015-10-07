rm -rf ../localbudgets-db/*
python manage.py upload_budget
python manage.py tree_schema
python manage.py muni2tree
