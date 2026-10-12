# Egress proxy for agent containers: only the two model APIs are reachable.
FROM alpine:3.20
RUN apk add --no-cache tinyproxy
COPY tinyproxy.conf filter /etc/tinyproxy/
EXPOSE 8888
CMD ["tinyproxy", "-d", "-c", "/etc/tinyproxy/tinyproxy.conf"]
