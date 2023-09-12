#base image
FROM python:3.10
# -----------------------------------
# switch to application directory
WORKDIR /app
# -----------------------------------
# create required folder
#RUN mkdir /app
# -----------------------------------
# Copy required files from repo into image

COPY ./ /app/

# -----------------------------------
# update image os
RUN apt-get update

RUN pip install cudatoolkit=11.2
# -----------------------------------
# environment variables
ENV PYTHONUNBUFFERED=1

# -----------------------------------
# run the app (re-configure port if necessary)
EXPOSE 5000

CMD ["python", "Publisher.py"]
