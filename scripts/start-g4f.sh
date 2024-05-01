#!/bin/bash
docker run -p 127.0.0.1:9080:8080 --name g4f -p 127.0.0.1:1337:1337 -p 127.0.0.1:7900:7900 --shm-size="2g" -v ${PWD}/hardir:/app/hardir hlohaus789/g4f:latest
