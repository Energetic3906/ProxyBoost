## 运行

```yaml
services:
  proxyboost:
    image: povoma4617/proxyboost:latest
    container_name: proxyboost
    ports:
      - "127.0.0.1:30830:30830"
    restart: always
```

## Nginx 反代

```conf
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    listen 443 quic;
    listen [::]:443 quic;
    # To support HTTP/2
    http2 on;
    
    # Quic or HTTP/3 response header
    add_header Alt-Svc 'h3=":443"; ma=86400';
    server_name your.domain.com;

    # SSL
    ssl_certificate         /etc/nginx/ssl/your.domain.com/fullchain.cer;
    ssl_certificate_key     /etc/nginx/ssl/your.domain.com/your.domain.com.key;
    ssl_trusted_certificate /etc/nginx/ssl/your.domain.com/fullchain.cer;

    # security
    include                 nginxconfig.io/security.conf;

    # logging
    access_log              /var/log/nginx/your.domain.com_access.log combined buffer=512k flush=1m;
    error_log               /var/log/nginx/your.domain.com_error.log warn;

    # reverse proxy
    location / {
        proxy_pass            http://127.0.0.1:30830;
        proxy_set_header Host $host;
        include               nginxconfig.io/proxy.conf;
    }

    # additional config
    include nginxconfig.io/general.conf;
}

# HTTP redirect
server {
    listen      80;
    listen      [::]:80;
    server_name your.domain.com;

    location / {
        return 301 https://your.domain.com$request_uri;
    }
}
```

## 使用

如果访问：

```md
https://raw.githubusercontent.com/Energetic3906/ProxyBoost/main/main.py
```

那么通过 ProxyBoost 访问的方式：

```md
https://your.domain.com/https://raw.githubusercontent.com/Energetic3906/ProxyBoost/main/main.py
```
