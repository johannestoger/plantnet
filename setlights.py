#!/usr/bin/env python3
"""Provide a CLI for Tradfri."""
import logging
from pprint import pprint
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

    host = '192.168.15.11'
    with open('gateway.key', 'r') as keyfile:
        gateway_key = keyfile.read().replace('\n','')

    logging.basicConfig(filename='plantnet.log', level=logging.INFO)

    api = api_factory(host, gateway_key)
    gateway = Gateway()
    devices_commands = api(gateway.get_devices())
    devices = api(*devices_commands)
    lights = [dev for dev in devices if dev.has_light_control]
    light = lights[0]
    groups = api(gateway.get_groups())
    group = groups[0]
    moods = api(gateway.get_moods())
    mood = moods[0]
    tasks = api(gateway.get_smart_tasks())

    # Compute light level for current time
    tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    now = datetime.datetime.now(tz)

    starttime = now.replace(hour=10, minute=28, second=0, microsecond=0)
    endtime = now.replace(hour=10, minute=35, second=0, microsecond=0)

    light_on = 10
    light_off = 0
    light_setlevel = light_off

    if now >= starttime and now <= endtime:
        light_setlevel = light_on

    # Set lights
    logstr = 'plantnet {}: Setting lights to {}'.format(time.strftime('%c'), light_setlevel)
    logging.info(logstr)

    for light in lights:
        api(light.light_control.set_dimmer(light_setlevel))

#print()
#print("Example commands:")
#print("> devices")
#print("> light.light_control.lights")
#print("> api(light.light_control.set_dimmer(10))")
#print("> api(light.light_control.set_dimmer(254))")
#print("> api(light.light_control.set_xy_color(254))")
#print("> api(lights[1].light_control.set_dimmer(20))")
#print("> tasks[0].repeat_days_list")
#print("> groups")
#print("> moods")
#print("> tasks")
#print("> dump_devices()")
#print("> dump_all()")

main()
