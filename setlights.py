#!/usr/bin/env python3

import logging
import sys
import os
import datetime
import time

here_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(here_path)
sys.path.append('pytradfri')

from pytradfri.const import *  # noqa
from pytradfri.api.libcoap_api import api_factory
from pytradfri.gateway import Gateway
from pytradfri.command import Command


def main():
    logging.basicConfig(filename='plantnet.log', level=logging.INFO)

    # api setup
    host = '192.168.15.11'
    with open('gateway.key', 'r') as keyfile:
        gateway_key = keyfile.read().replace('\n','')
    api = api_factory(host, gateway_key)
    gateway = Gateway()
    devices_commands = api(gateway.get_devices())
    devices = api(*devices_commands)
    lights = [dev for dev in devices if dev.has_light_control]


    # Compute light level for current time -- lights should be on during the night
    # so our time coordinate is in *hours since last noon*.
    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    now = datetime.datetime.now(tz)

    # reference time: last noon
    noontoday = now.replace(hour=12, minute=0, second=0, microsecond=0) # noon today
    if now > noontoday: # pm
        lastnoon = noontoday;
    elif now < noontoday: # am
        lastnoon = noontoday - datetime.timedelta(days=1)
    else: # exactly noon, quite unlikely but let's handle it
        lastnoon = noontoday

    tc = (now-lastnoon).total_seconds()/3600.0; # time coordinate: hours since last noon

    starttime = 10 # lights on 10pm
    endtime = 12+6.5 # lights off 6:30 am

    light_on = 254
    light_off = 0

    # TODO: Fancy gradual increase/decrease of lights instead of sharp on/off
    light_setlevel = light_off
    if tc >= starttime and tc <= endtime:
        light_setlevel = light_on

    # Set lights
    logstr = 'plantnet {}: tc = {:0.2f}, setting lights to {}'.format(time.strftime('%c'), tc, light_setlevel)
    logging.info(logstr)

    for light in lights:
        api(light.light_control.set_dimmer(light_setlevel))

main()
