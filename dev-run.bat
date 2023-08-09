@echo off
pip install -r requirements.txt
pip install -r requirements_dev.txt

echo "Formatting using black"
black -t py310 src
echo "Formating using isort"
isort src
echo "################################### PYLINT ########################"
pylint src
echo "################################### PYTEST ########################"
pytest
cd docs
make html
cd..