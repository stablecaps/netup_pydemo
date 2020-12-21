# NetUp

## Overview

A Python3 script to check network connectivity and suggest possible reasonsfor lost connectivity. Tested working on Ubuntu 20.04.

## Dependencies

Formatting & colour works best with green on black background. With anything else, your mileage may vary!

```
python3.8
python3.8-vemv
route
nmcli

```

## Usage


#### simulate dns fail
https://serverfault.com/questions/776049/how-to-simulate-dns-server-response-timeout
What you need is a "black hole server". You can use blackhole.webpagetest.org (72.66.115.13) which will silently drop all requests.

Why I suggest this over the other answers, is because the aforementioned server has been established for this sole purpose.
