FROM ubuntu:20.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN git clone https://github.com/abdullahzamanbabar/syntribos.git
RUN python3 -m pip install /syntribos
RUN yes | syntribos init
RUN sed -i 's|endpoint=.*|endpoint=https://l2qs966u0c.execute-api.us-east-2.amazonaws.com|' $(syntribos root)/syntribos.conf
RUN printf "GET /prod/health HTTP/1.1\nContent-Type: application/json" > $(syntribos root)/templates/health_check.template
RUN printf "GET /prod/urls HTTP/1.1\nContent-Type: application/json" > $(syntribos root)/templates/urls_check.template
RUN syntribos --config-file $(syntribos root)/syntribos.conf run

COPY script.sh /script.sh

CMD ["/bin/bash", "script.sh"]