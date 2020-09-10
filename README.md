# Garage

Okay so this got to be a bit more complicated then I had originally intended. Turns out the
micropython library for mozilla-iot webthings cannot run on an ESP8266 (it can run on an ESP32).
So I have a very lightweight API running on the ESP8266 and then I have a docker container running
the mozilla webthings as a proxy to the ESP8266 API. This is not ideal, but does work.

## Micropython Code

So the src folder contains the code that is deployed to the ESP8266. Some of the files are to large
to be compiled on the ESP8266. So I am compiling them to .mpy files in the dist folder. The main.py
cannot be compiled because it is the entrypoint file that micropython is looking for. I use mpy-cross
to compile the python scripts and compiled it myself and have it as part of this repo but you may need
to recompile it yourself for it to work on your machine


## Setup the development environment

First setup the pipenv virtual environment with the development dependencies.

```shell script
pipenv install --dev
```

Then set up so your user has permissions to the `dialout` group (TTY permissions). 
**you probably need to log out and back in for this to take effect**

```shell script
sudo usermod -a -G dialout $USER
```

## Setting up the ESP8266

1. Prepare the ESP8266 by first erasing the flash by running
   ```shell script
   pipenv run erase
   ```

1. Flash micropython to the ESP8266 by running
   ```shell script
   pipenv run flash
   ```

## Playing around with the ESP8266

You can run the micropython repl by running the following command. (this starts a repl using `rshell`) 

```shell script
pipenv run repl
```

## Deploying to the ESP8266

1. Compile the python code in the `src` folder by running
   ```shell script
   pipenv run compile
   ```

1. Deploy the code in the `dist` folder by running
   ```shell script
   pipenv run compile
   ```

## Wiring setup on the ESP8266

So I have tried this code out on 2 different ESP8266 that I got on Amazon and they both work great. I used
the first one in a bread board for figuring it out and then the second one I mounted to a proto board and
for the final product.   

https://www.amazon.com/gp/product/B07HF44GBT/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1   
https://www.amazon.com/gp/product/B076F53B6S/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1

I then wired the following sensor to PIN 12 and ground.   

https://www.amazon.com/gp/product/B07DBP7QLT/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1   

And finally wired the following relay to PIN 14 and also to the Vin and ground.   

https://www.amazon.com/gp/product/B07WQH63FB/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1


## Some additional details

So I guess to explain everything else.. I have the MAC address of my ESP8266 in my router assigning a 
static IP address which I have an internal DNS address map to that IP address for garage.home.internal.
So then my docker webthings proxy just polls the ESP8266 API to read the open or closed status. And then
sends the toggle command to the ESP8266 API when it needs to from the iot gateway.   

I have the mozilla-iot gateway also running in another container behind my traefik load balancer and that
is what I actually use from my phone to connect to the proxy webthings container and then finally to the
ESP8266. The mozilla-iot gateway is not perfect, and I am working on figuring out how best to define my
webthing. But the gateway has some very nice features like rules so that you can send a notification to
yourself if the door is left open after X'o clock or even just have it automatically close it. 
