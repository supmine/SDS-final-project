FROM node:19-alpine AS builder

WORKDIR /app

COPY package.json .

RUN yarn install

COPY . .

RUN yarn build

FROM nginx:stable-alpine

WORKDIR /usr/share/nginx/html

COPY --from=builder /app/build .

COPY ./default.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]