FROM rasa/rasa-sdk:3.0.0

#define the working directory of Docker container
WORKDIR /app 
#copy the requirements txt file with your dependencies in actions directory
COPY ./requirements-actions.txt ./ 
#copy everything in ./actions directory (your custom actions code) to /app/actions in container
# COPY ./ /app/actions
COPY actions.py /app
# COPY stanzatokenizer.py /app
# COPY dbQueries.py /app
COPY advisors.db /app
#install dependencies inside Docker container
USER root 
RUN pip3 install -U pip
RUN pip3 install -r requirements-actions.txt
USER 1001 
