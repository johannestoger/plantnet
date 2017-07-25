"""Provide a CLI for Tradfri."""
import logging
from pprint import pprint
import sys

sys.path.append('pytradfri')

from pytradfri.const import *  # noqa
from pytradfri.api.libcoap_api import api_factory
from pytradfri.gateway import Gateway
from pytradfri.command import Command


def main():

    host = '192.168.15.11'
    with open('gateway.key', 'r') as keyfile:
        gateway_key = keyfile.read().replace('\n','')

    logging.basicConfig(level=logging.DEBUG)

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


    for light in lights:
        api(light.light_control.set_dimmer(int(sys.argv[1])))

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
