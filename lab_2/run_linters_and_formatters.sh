black *.py pyobjserializer/*.py
isort *.py pyobjserializer/*.py
mypy *.py pyobjserializer/*.py
flake8 --max-line-length 120 *.py pyobjserializer/*.py
pydocstyle *.py ./pyobjserializer/*.py
