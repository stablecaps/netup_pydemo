# NetUp

## Overview

A Python3 script to check network connectivity and suggest possible reasonsfor lost connectivity. Tested working on Ubuntu 20.04.

## Dependencies

Formatting & colour works best with green on black background. With anything else, your mileage may vary!

```
Tested on ubuntu 20.04
python3.8
python3.8-vemv
route (built into 20.04)
nmcli (built into 20.04)
nc (netcat)
traceroute
```

## Install
```
sudo apt install python3.8 python3.8-venv python3.8-venv netcat traceroute
```

```
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
# Launch publicip subroutine
python netup_luncher.py publicip

# Launch connection subroutine
python netup_luncher.py connx

# Launch dns server checker subroutine
python netup_luncher.py dns

# Launch traceroute subroutine
python netup_luncher.py traceroute

# Launch all routines
python netup_luncher.py all

```

#### simulate dns fail
https://serverfault.com/questions/776049/how-to-simulate-dns-server-response-timeout
What you need is a "black hole server". You can use blackhole.webpagetest.org (72.66.115.13) which will silently drop all requests.

Why I suggest this over the other answers, is because the aforementioned server has been established for this sole purpose.
