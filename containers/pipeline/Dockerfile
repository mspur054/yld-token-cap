FROM python:3.9.5

WORKDIR /code
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/code/src


# Update args in docker-compose.yaml to set the UID/GID of the "vscode" user.
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; then groupmod --gid $USER_GID vscode && usermod --uid $USER_UID --gid $USER_GID vscode; fi


# cron
RUN apt-get -y update && apt-get install -y cron

# copy code

COPY ./ /code/


# Python requirements
RUN pip install --upgrade pip

COPY ./containers/pipeline/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY /cron/get_yld_token_info /etc/cron.d/get_yld_token_info


# Move environment variables to file
COPY /cron/start_env.sh /etc/start_env.sh

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/get_yld_token_info

# Apply cron job
RUN crontab /etc/cron.d/get_yld_token_info

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
# Run cron
CMD ["/etc/start_env.sh"]