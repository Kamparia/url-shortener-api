# set base image (host OS)
FROM python:3.9

# set working directory
WORKDIR /code

# install dependencies - copy the dependencies file to the working directory
COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

# copy the content of the local scripts directory to the working directory
COPY . /code

# command to run on container start
CMD ["uvicorn", "main:app"]