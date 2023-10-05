FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python3 -m unidic download

# 
COPY ./main.py /code/

# 
CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
