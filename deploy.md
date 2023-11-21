# Deploy Your Own

## prerequisite

docker compose & python3

## Deploy

For better experience, We strongly suggest you use Docker. 

Clone this repo. 

```bash
git clone https://github.com/usexhs/xhs-link.git
cd xhs-link/src
```

### w/o Proxy

The default config presumes a socks5 proxy. If you do not want to use a proxy, comment out the proxy settings in `main.py`. 

```diff
    proxies = {
-        'http': f'socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
-        'https': f'socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}',
    }
```

### w/ Proxy

If you choose to use a socks5 proxy, please setup the proxy in `docker-compose.yml`. 

Especially, when you run the proxy in a Docker container, please add the network of this container to the network of the proxy container.[^1] For example: 

```diff

+networks:
+  proxy-net:
+    driver: bridge
+    name: proxy_network


services:
  proxy-example:
    container_name: proxy_container
+    networks:
+     - proxy-net
```

Then edit `docker-compose.yml`. Use the `container_name` of the proxy for `PROXY_HOST`, as well as the exposed port **INSIDE** that container for `PROXY_PORT`. For example: 

```diff
+networks: 
+  xhs-link-proxy:
+    external: true
+    name: proxy_network

services:
  xhs-link: 
+    networks:
+     - xhs-link-proxy
    environment:
-      PROXY_HOST: ""
+      PROXY_HOST: "proxy_container"
-      PROXY_PORT: ""
+      PROXY_PORT: "YOUR_PORT"
```

### Start Container

Finally, bring up the container. 

```bash
docker compose build
docker compose up -d
```

### Reverse Proxy

Then the service should be available at "127.0.0.1:5000" of your server. We strongly suggest you use a reserve proxy. Here's a basic example of corresponding `nginx`. 

```nginx
# nginx.conf

server {
    listen 80;
    server_name your_domain.com;  # Change this to your domain or IP address

    location / {
        proxy_pass http://127.0.0.1:5000;  
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Additional configurations can be added as needed
}

```

[^1]: https://www.baeldung.com/ops/docker-compose-communication