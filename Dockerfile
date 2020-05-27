FROM python:3.7-stretch
WORKDIR /app
COPY . /app/
RUN make flake8
RUN make test
RUN ./ve/bin/pip install psycopg2-binary
EXPOSE 8000
ADD docker-run.sh /run.sh
ENV APP capsim
ENTRYPOINT ["/run.sh"]
CMD ["run"]
