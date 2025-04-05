# stable-20191118
FROM debian as builder
RUN apt-get update && apt-get install -y musl-tools
WORKDIR /build
ADD readflag.c .
RUN musl-gcc -s -oreadflag -Os -static readflag.c

FROM php:8.3-apache as app

# set recommended PHP.ini settings
# see https://secure.php.net/manual/en/opcache.installation.php
RUN { \
		echo 'opcache.memory_consumption=128'; \
		echo 'opcache.interned_strings_buffer=8'; \
		echo 'opcache.max_accelerated_files=4000'; \
		echo 'opcache.revalidate_freq=60'; \
		echo 'opcache.fast_shutdown=1'; \
		echo 'opcache.enable_cli=1'; \
	} > /usr/local/etc/php/conf.d/opcache-recommended.ini

WORKDIR /var/www/html

RUN apt-get update \
    && apt-get install -y git nano wget \
    && docker-php-ext-install mysqli \
    && apt-get clean all \
	&& git clone --depth 1 https://github.com/KevinKate/flightbook \
	&& sed -i "s/header('main.php?page=main');//g" flightbook/index.php \
	&& sed -i "s/('localhost','root','','book')/('mysql','root','','book')/g" flightbook/*.php \
	&& echo "$(tail -n +2 flightbook/index.php)" > flightbook/index.php\
    && mv flightbook/* . \
    && rm -rf flightbook \
    && chown -R www-data:www-data . \
    && chmod -R 755 /var/www/html 

COPY flag.txt /flag.txt
COPY --from=builder --chown=root:root /build/readflag /

RUN chmod u=srx,g=rx,o=x /readflag
RUN chmod 0400 /flag.txt
 
USER www-data
EXPOSE 80 443
CMD ["apache2-foreground"]