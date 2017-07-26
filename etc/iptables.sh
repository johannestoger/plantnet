#!/bin/bash

LOCAL=br0
WORLD=wlan1

sudo iptables -t nat -A POSTROUTING -o ${WORLD} -j MASQUERADE
sudo iptables -A FORWARD -i ${WORLD} -o ${LOCAL} -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i ${LOCAL} -o ${WORLD} -j ACCEPT
