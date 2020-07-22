
FROM node:14-alpine as builder

COPY . .

ARG MODE=production

RUN npm run build -- --mode ${MODE}


RUN ls -la dist
# --output js/main.js



FROM nginx:1.17-alpine

RUN mkdir /usr/share/nginx/html/js

COPY --from=builder dist /usr/share/nginx/html

RUN ls /usr/share/nginx/html



EXPOSE 80 443