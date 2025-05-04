FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Update and install required packages
RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    python3 \
    cron \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure Apache
# The correct module name is php7.4 or php8.1 depending on the version installed
RUN a2enmod php8.1 || a2enmod php7.4 || true
RUN a2enmod rewrite
RUN sed -i 's/DirectoryIndex index.html/DirectoryIndex index.php index.html/' /etc/apache2/mods-enabled/dir.conf

# Set up scripts directory
RUN mkdir -p /opt/scripts/ && chmod 755 /opt/scripts/ && chown root:root /opt/scripts/
COPY osinfo.py /opt/scripts/osinfo.py
RUN chmod 755 /opt/scripts/osinfo.py

# Set environment variables
RUN echo "PYTHONUSERBASE=/tmp" >> /etc/environment

# Set up cron job
RUN printf "* * * * * root /usr/bin/python3 /opt/scripts/osinfo.py\n" > /etc/cron.d/python-cron && chmod 0644 /etc/cron.d/python-cron

# Create the flag file
RUN FILENAME=$(openssl rand -hex 12).txt && echo "DDC{eksempel}" > /root/$FILENAME

# Configure Apache document root
RUN rm -rf /var/www/html/*

# Copy PHP files from src directory
COPY src/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html/

# Expose port 80
EXPOSE 80

# Start Apache and cron
CMD service cron start && apache2ctl -D FOREGROUND
