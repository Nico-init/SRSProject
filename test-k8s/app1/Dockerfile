FROM python:3.11.0b1-alpine3.15

ENV MY_PARAM1=gianni
RUN mkdir -p /home/app
COPY . /home/app

WORKDIR /home/app
# RUN viene eseguito nel container sui layer definiti sopra, per poi andare a costruire l'immagine finale
# Non verra' eseguito al momento del deployment. L'unica cosa che eseguie al deployment
# e' CMD
RUN python3 myIP.py > outIP.txt
CMD ["sleep", "3600d"]
#CMD [ "python3", "test.py" ]   #facengo kubectl log sul nodo vedo l'output dato dal comando