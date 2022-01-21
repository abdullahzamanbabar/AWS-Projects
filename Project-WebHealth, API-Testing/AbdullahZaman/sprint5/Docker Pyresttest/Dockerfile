FROM ubuntu:20.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python2
RUN apt-get install -y pip
RUN apt-get install -y git
RUN apt-get install -y python-pycurl
RUN apt-get install -y python-yaml
RUN git clone https://github.com/svanoort/pyresttest.git
RUN cd pyresttest && python2 setup.py install && cd ../
COPY apiTest.yaml /apiTest.yaml
RUN pyresttest https://s7rt0vfv66.execute-api.us-east-2.amazonaws.com apiTest.yaml
COPY script.sh /script.sh

CMD ["/bin/bash","script.sh"]

