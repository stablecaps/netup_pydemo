# NetUp Demo - 2020 (A Timed Interview Test ~10 days)

## Overview

A Python3 program to check network connectivity and suggest possible reasons for lost connectivity. Tested working on Ubuntu 20.04.

Write a script using Python that:
1. Determines the state of Internet connectivity.
2. If a loss of connectivity is detected, determines the cause and reports it.
3. For as many causes as possible, suggests a fix.
4. Sets the script’s exit status to indicate whether or not Internet connectivity was present

#### Note: This code has been written to showcase my Python3 dev skills, so yes, I went OTT! :)

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
dig
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

## Run all tests
```
pytest

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

# Launch all routines and force initial error so all routines are run
python netup_luncher.py all --force true

```

### Simulating Failure:

#### Trigger start of test routine:

```

## ~Change line 99 to:~
~tcp_ping_commm = "nc -vz -w 5 www.google.com 8080"~

now use:
python netup_luncher.py all --force true
```

#### Check connectivity
Disconnect network connection

#### Test local issue
Block TCP/UDP on router so at least one hop is made

#### DNS fail
https://serverfault.com/questions/776049/how-to-simulate-dns-server-response-timeout
What you need is a "black hole server". You can use blackhole.webpagetest.org (72.66.115.13) which will silently drop all requests.


## Things left to do
Quite a fun test, but I would have liked a bit more time to thoroughly test the script so more definitive exit points (with status codes) could be made. This would involve testing connectivity via various protocols and figuring out how to implement that for testing.

I would also have liked to write more tests to check the functionality of the program given enough time.