FROM python:3
Run mkdir /OnlineShopping
WORKDIR /OnlineShopping
ADD . /OnlineShopping
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "base.py"]



