FROM node:16-alpine

WORKDIR /client

ENV PATH /client/node_modules/.bin:$PATH

COPY package.json ./
COPY yarn.lock ./
COPY tsconfig.json ./
COPY .env ./
COPY ./src ./src

RUN yarn add node-sass

RUN yarn install


EXPOSE 2000

CMD ["echo", "Dependencies installed"]

CMD bash