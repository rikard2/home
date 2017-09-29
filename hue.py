#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import soco
import datetime
from soco import SoCo
from soco.data_structures import DidlItem, DidlResource
from soco.music_services import MusicService
from soco.compat import quote_url
from dateutil import parser

import json
import time

autumn_chill                    = 'spotify:user:mariokristian:playlist:7G8qKmsQOGyguhiEo2o8bl'
motion_sensor_name              = 'Hue motion sensor 1'
sonos_speaker_name              = 'PlaybarVardagrum'
motion_sensor_min_diff_seconds  = 10 # 60 * 60 * 2 # 2 hours
username                        = 'pgq82ZreITIUSmNSpaerNDJ3pH1emTi3R-65g-CU'

def add_from_service(item_id, service, device, is_track=True):

    item_id = quote_url(item_id.encode('utf-8'))
    didl_item_id = "0fffffff{0}".format(item_id)

    # For an album:
    if not is_track:
        uri = 'x-rincon-cpcontainer:' + didl_item_id

    else:
        # For a track:
        uri = service.sonos_uri_from_id(item_id)

    res = [DidlResource(uri=uri, protocol_info="DUMMY")]
    didl = DidlItem(title="DUMMY",
        # This is ignored. Sonos gets the title from the item_id
        parent_id="DUMMY",  # Ditto
        item_id=didl_item_id,
        desc=service.desc,
        resources=res)

    device.add_to_queue(didl)

def coming_home():
    speakers = soco.discover()
    if (speakers == None):
        print("Couldn't discover sonos speakers...")
        return
    speaker = None
    for s in speakers:
        if (s.player_name == sonos_speaker_name):
            speaker = s
    if (speaker == None):
        print("Couldn't discover sonos speakers...")
        return
    sonos = SoCo(speaker.ip_address)
    print("Found Sonos Speaker " + speaker.player_name)
    service = MusicService("Spotify")
    sonos.play_mode = 'SHUFFLE'
    sonos.partymode()
    sonos.clear_queue()
    sonos.stop()
    add_from_service(autumn_chill, service, sonos, False)
    sonos.play()

def nupnp():
    response = requests.get('https://www.meethue.com/api/nupnp');
    response_json = json.loads(response.text)

    bridge_ip = response_json[0]['internalipaddress'];
    print("Found HUE bridge " + bridge_ip)
    return bridge_ip

def clip(type, bridge_ip, path, request_json = None):
    if type == 'GET':
        response = requests.get('http://' + bridge_ip + '/' + path);
        response_json = json.loads(response.text)

        return response_json
    elif type == 'POST':
        response = requests.post('http://' + bridge_ip + '/' + path, json = request_json);
        response_json = json.loads(response.text)
    elif type == 'PUT':
        response = requests.put('http://' + bridge_ip + '/' + path, json = request_json);
        response_json = json.loads(response.text)

        return response_json

def connect(bridge_ip):
    for x in range(0, 10):
        r = clip('POST', bridge_ip, 'api', { "devicetype": "gohue#Rikard macbook" } )
        r = r[0]

        if ('error' in r):
            if (x == 0):
                print("Press the button")
        elif ('success' in r):
            username = r['success']['username']
            print("Found username " + username)
            return username
        else:
            print("wtf?")
        time.sleep(1)

def turn_on(bridge_ip, username):
    action = {"on":True,"bri":255,"sat":255,"hue":0}
    action = { "scene": "yzgwmzWucuTJcyX" }
    r = clip('PUT', bridge_ip, 'api/' + username + '/groups/6/action', action)

def motion(bridge_ip, username):
    last_state = False
    last_updated = None
    while True:
        r = clip('GET', bridge_ip, 'api/' + username + '/sensors')
        if (len(r) == 1):
            if ('error' in r[0]):
                print("ERROR")
        for key in r:
            if (r[key]["name"] == motion_sensor_name):
                new_lastupdated = parser.parse(r[key]["state"]["lastupdated"])
                new_state = r[key]["state"]["presence"]
                if (new_state != last_state):
                    if (last_updated != None):
                        diff = new_lastupdated - last_updated
                        if (diff.total_seconds() > motion_sensor_min_diff_seconds and new_state == True):
                            print("Coming home!")
                            turn_on(bridge_ip, username)
                            coming_home()
                    last_state = r[key]["state"]["presence"]
                if (last_updated != new_lastupdated):
                    last_updated = new_lastupdated
        time.sleep(1)

bridge_ip = nupnp()
# username = connect(bridge_ip)
motion(bridge_ip, username)
#coming_home()
