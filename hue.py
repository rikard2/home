#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import soco
from datetime import datetime, timedelta
from soco import SoCo
from soco.data_structures import DidlItem, DidlResource
from soco.music_services import MusicService
from soco.compat import quote_url
from dateutil import parser

import json, time, re
import playlist
motion_sensor_name              = 'Hall motion sensor'
sonos_speaker_name              = 'PlaybarVardagrum'
motion_sensor_min_diff_seconds  = 60 * 60 * 4 # 2 hours
username                        = 'pgq82ZreITIUSmNSpaerNDJ3pH1emTi3R-65g-CU'
speakers_volume                 = 20
scene_id                        = '33300ac17-on-0'

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
        s.volume = speakers_volume
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
    chosen_playlist = playlist.choose()
    if chosen_playlist is not None:
        add_from_service(chosen_playlist, service, sonos, False)
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

def turn_on_light(bridge_ip, username):
    #action = {"on":True,"bri":255,"sat":255,"hue":0}
    action = { "scene": scene_id }
    r = clip('PUT', bridge_ip, 'api/' + username + '/groups/8/action', action)

def motion(bridge_ip, username):
    last_state = False
    previous_state_change = datetime.utcnow() + timedelta(hours=2)

    while True:
        r = clip('GET', bridge_ip, 'api/' + username + '/sensors')
        if (len(r) == 1):
            if ('error' in r[0]):
                print("ERROR")
        for key in r:
            if (r[key]["name"] == motion_sensor_name):
                (year, month, day, hour, minute, second) = re.search('(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})', r[key]["state"]["lastupdated"]).groups()
                state_change = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)) + timedelta(hours=2)
                new_state = r[key]["state"]["presence"]
                diff = state_change - previous_state_change
                if (new_state != last_state):
                    if new_state == True:
                        print("Motion sensor triggered, diff is {} seconds.".format(round(diff.total_seconds(), 0)))
                        print("Am I coming home? {} > {}".format(round(diff.total_seconds(), 0), motion_sensor_min_diff_seconds))
                        if int(diff.total_seconds()) > motion_sensor_min_diff_seconds:
                            print("Coming home!")
                            previous_state_change = state_change
                            turn_on_light(bridge_ip, username)
                            coming_home()
                    last_state = r[key]["state"]["presence"]

        time.sleep(1)

#bridge_ip = nupnp()
# username = connect(bridge_ip)
turn_on_light('ricksplace.zapto.org:12222', username)
#motion('ricksplace.zapto.org:12222', username)
