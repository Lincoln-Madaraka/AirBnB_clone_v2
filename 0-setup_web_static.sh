#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static
# install nginx
sudo apt-get -y update
sudo apt-get -y install nginx
# Create the folder /data/ if it doesn’t already exist
# Create the folder /data/web_static/ if it doesn’t already exist
# Create the folder /data/web_static/releases/ if it doesn’t already exist
sudo mkdir -p /data/web_static/releases/
# Create the folder /data/web_static/shared/ if it doesn’t already exist
sudo mkdir -p /data/web_static/shared/
# Create the folder /data/web_static/releases/test/ if it doesn’t already exist
sudo mkdir -p /data/web_static/releases/test/
# Create a fake HTML file /data/web_static/releases/test/index.html
echo "Hello world!" | sudo tee /data/web_static/releases/test/index.html
# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/
# update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
LOCATION="location /hbnb_static {\n\t\t alias /data/web_static/current/;\n}\n"
sudo sed -i "/server_name _;/a $LOCATION" "/etc/nginx/sites-available/default"
# restart nginx
sudo service nginx restart

