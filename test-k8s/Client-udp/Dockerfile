FROM python:3.11.0b1-alpine3.15

ENV SERVER_IP="172.17.0.2"
#ENV SERVER_IP="server"

RUN mkdir -p /home/client
COPY Client.py /home/client

WORKDIR /home/client
# RUN viene eseguito nel container sui layer definiti sopra, per poi andare a costruire l'immagine finale
# Non verra' eseguito al momento del deployment. L'unica cosa che eseguie al deployment
# e' CMD
#RUN python3 myIP.py > outIP.txt

#CMD ["sleep", "3600d"]
CMD [ "python3", "Client.py" ]
#facengo kubectl log sul nodo vedo l'output dato dal comando