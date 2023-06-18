# The script uses the certbot arm docker image so if you have to use it in another architecture change that :D
#
# An easy to use docker based script that using the Clouldflare API and Let's Encrypt will generate a valid pkcs12 
# file that can be used to configure a custom domain in a Plex Media Server. Make sure you create a cloudflare.ini 
# file with a valid Cloudflare API token in it and change the DOMAIN variable in the generate_plex_certificate.sh file.

#! /bin/bash

DOMAIN=plex.domain.com

echo "Generating lets encrypt certificate..."
docker run -it --rm --name certbot \
  -v "$(pwd)/letsencrypt:/etc/letsencrypt" \
  -v "$(pwd)/letsencrypt:/var/lib/letsencrypt" \
  -v "$(pwd)/cloudflare.ini:/cloudflare.ini" \
  certbot/dns-cloudflare:arm32v6-latest certonly --dns-cloudflare \
  --dns-cloudflare-credentials /cloudflare.ini -d $DOMAIN

echo "Cleaning Docker image..."
docker image rm certbot/dns-cloudflare:arm32v6-latest

echo "Preparing Plex certificate...""
sudo openssl pkcs12 -export -in letsencrypt/live/$DOMAIN/fullchain.pem \
   -inkey letsencrypt/live/$DOMAIN/privkey.pem -out certificate.pfx
sudo chown pi:pi certificate.pfx
echo "Done!"
# Example of the cloudflare.ini file
## Cloudflare API token used by Certbot
#dns_cloudflare_api_token = 0123456789abcdef0123456789abcdef01234567
