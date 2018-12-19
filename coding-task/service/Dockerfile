FROM php:7.3-apache
RUN a2enmod rewrite

WORKDIR /var/www/html/
ENV HOME /var/www/html/

# copy the app
COPY . .
