#!/bin/bash

docker run -v $(pwd):/var/loadtest -v $HOME/.ssh:/home/yandextank/.ssh --dns 192.168.95.254 -it direvius/yandex-tank