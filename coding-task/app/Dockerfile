FROM php:7.3-fpm-alpine

COPY --from=composer:1.8 /usr/bin/composer /usr/bin/composer

WORKDIR /app
ENV HOME /app
RUN chown nobody /app
USER nobody

# install dependencies
COPY composer.json .
RUN composer install

# copy the rest of the app
COPY . .

RUN php -m