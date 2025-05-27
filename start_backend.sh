#!/bin/bash
#gnome-terminal -t "pypy3" -x bash -c "pypy3;exec bash;"
{
	echo "Lunching python"
	cd 	/codes/AIGC_backend/AIGC_backend/AIGC_backend/AIGC_backend/
	pip install -r requirements.txt
	cd 	/codes/AIGC_backend/AIGC_backend/AIGC_backend/AIGC_backend/aigcBackend/
	python manage.py runserver 0.0.0.0:8000
}


wait