Coding task
===========

This repository contains a small PHP application that is run by [`docker-compose`](https://docs.docker.com/compose/):

* `app` container is a simple PHP application that is served via nginx on port 8080.
* `service` container should be treated as a 3rd party service that we want to interact with.

`docker-compose build && docker-compose up` builds and runs our application.
You can now visit [0.0.0.0:8080](http://0.0.0.0:8080/).

# Your task

We want our `app` to provide a simple UI for the user to be able to store a given message in 3rd party service
and later retrieve it. Service requires an API token to be passed via `X-Token` request header. Token's value is provided
below in "Service API" section. You should store it securely and not expose it to the front-end layer of our application.
Hence, your task is to implement a PHP client that will act as a bridge between our user and the 3rd party service.
You will also need to implement a simple UI with AJAX interactions using jQuery.

We are aware that 3rd party service is a bit unreliable and sometimes responds with HTTP 502 error.
You need to handle that as well. After all, we do not want to annoy our users, do we? :)

Please submit your solution as a pull request to this repository. Good luck!

# API

## "3rd party" service API

The service listens on port `8080` and you can communicate with it using HTTP protocol.

All responses are JSON encoded. HTTP 401 response will be served when `X-Token` header is missing or is invalid.
HTTP 502 indicates that the server was not able to process the request and the client should retry it.

**Our token**: `0d5f153fb24410ec8c83092b976ac8205cd4a302`.

### `GET /`

```
$ curl 'http://0.0.0.0:8088' -sv | jq
* Rebuilt URL to: http://0.0.0.0:8088/
*   Trying 0.0.0.0...
* Connected to 0.0.0.0 (127.0.0.1) port 8088 (#0)
> GET / HTTP/1.1
> Host: 0.0.0.0:8088
> User-Agent: curl/7.47.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Thu, 20 Dec 2018 08:28:22 GMT
< Server: Apache/2.4.25 (Debian)
< X-Powered-By: PHP/7.3.0
< X-Limonade: Un grand cru qui sait se faire attendre
< Set-Cookie: LIMONADE0x5x0=c1fa69aafb05ed13e0fe92cb7e807e5e; path=/
< Expires: Thu, 19 Nov 1981 08:52:00 GMT
< Cache-Control: no-store, no-cache, must-revalidate
< Pragma: no-cache
< Content-Length: 80
< Content-Type: application/json; charset=utf-8
< 
{ [80 bytes data]
* Connection #0 to host 0.0.0.0 left intact
{
  "php_version": "7.3.0",
  "service_version": "0.1",
  "message_path": "/tmp/.message"
}
```

### `GET /message`

Gets previously stored message. `X-Token` header needs to be provided.

```
$ curl 'http://0.0.0.0:8088/message' -H 'X-Token: 0d5f153fb24410ec8c83092b976ac8205cd4a302' -v
*   Trying 0.0.0.0...
* Connected to 0.0.0.0 (127.0.0.1) port 8088 (#0)
> GET /message HTTP/1.1
> Host: 0.0.0.0:8088
> User-Agent: curl/7.47.0
> Accept: */*
> X-Token: 0d5f153fb24410ec8c83092b976ac8205cd4a302
> 
< HTTP/1.1 200 OK
< Date: Thu, 20 Dec 2018 08:26:15 GMT
< Server: Apache/2.4.25 (Debian)
< X-Powered-By: PHP/7.3.0
< X-Limonade: Un grand cru qui sait se faire attendre
< Set-Cookie: LIMONADE0x5x0=81efa4d779a7f5a9b1ec985c3f3a586e; path=/
< Expires: Thu, 19 Nov 1981 08:52:00 GMT
< Cache-Control: no-store, no-cache, must-revalidate
< Pragma: no-cache
< Content-Length: 17
< Content-Type: application/json; charset=utf-8
< 
* Connection #0 to host 0.0.0.0 left intact
{"message":"foo"}
```

### `POST /message`

Stores a message. `X-Token` header needs to be provided.

```
$ curl 'http://0.0.0.0:8088/message' -H 'X-Token: 0d5f153fb24410ec8c83092b976ac8205cd4a302' -d 'message=foo' -v
*   Trying 0.0.0.0...
* Connected to 0.0.0.0 (127.0.0.1) port 8088 (#0)
> POST /message HTTP/1.1
> Host: 0.0.0.0:8088
> User-Agent: curl/7.47.0
> Accept: */*
> X-Token: 0d5f153fb24410ec8c83092b976ac8205cd4a302
> Content-Length: 11
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 11 out of 11 bytes
< HTTP/1.1 202 Accepted
< Date: Thu, 20 Dec 2018 08:25:02 GMT
< Server: Apache/2.4.25 (Debian)
< X-Powered-By: PHP/7.3.0
< X-Limonade: Un grand cru qui sait se faire attendre
< Set-Cookie: LIMONADE0x5x0=e9bc89a1c990a679e856f6e9e721879d; path=/
< Expires: Thu, 19 Nov 1981 08:52:00 GMT
< Cache-Control: no-store, no-cache, must-revalidate
< Pragma: no-cache
< Content-Length: 0
< Content-Type: text/html; charset=UTF-8
< 
* Connection #0 to host 0.0.0.0 left intact
```