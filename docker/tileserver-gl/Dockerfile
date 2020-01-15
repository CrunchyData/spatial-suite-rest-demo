FROM node:12.13.0-buster

ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
# optionally if you want to run npm global bin without specifying path
ENV PATH=$PATH:/home/node/.npm-global/bin 

ENV MBTILES="/home/node/data/2017-07-03_california_santa-cruz.mbtiles"

COPY . /home/node/data

RUN npm install --unsafe-perm=true -g tileserver-gl-light && chmod -R 777 /home/node 

EXPOSE 8080

USER 1001

#VOLUME [ "${MBTILES}" ]

cmd ["bash", "-c", "tileserver-gl-light --mbtiles $MBTILES"]

