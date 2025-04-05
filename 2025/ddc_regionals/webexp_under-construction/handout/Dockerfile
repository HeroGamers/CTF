FROM php:7.4.21-cli
COPY index.php /var/www/site/index.php
COPY flag.txt /flag.txt
RUN mkdir /var/www/site/logs/
RUN chown -R www-data:www-data /var/www/site /flag.txt
USER www-data

EXPOSE 80
ENTRYPOINT ["php", "-d", "display_errors=off", "-S", "0.0.0.0:80", "-t", "/var/www/site/"]
