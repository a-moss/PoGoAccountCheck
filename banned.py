#!/usr/bin/python
# -*- coding: utf-8 -*-

"""banned.py - Check multiple PTC accounts ban status with Pokemon Go."""

from pgoapi import PGoApi
from pgoapi.utilities import f2i
from pgoapi import utilities as util
from pgoapi.exceptions import AuthException
from pgoapi.exceptions import ServerSideRequestThrottlingException
from pgoapi.exceptions import NotLoggedInException
import pprint
import time
import threading
import sys, getopt
import os

def check_account(username, password):
        api = PGoApi()
        auth = 'ptc'
        api.set_position(40.7127837, -74.005941, 0.0)
        if username.endswith("@gmail.com"):
            auth = 'google'
        if not api.login(auth, username, password):
            print "Failed to login the following account: {} (It may have been deleted)".format(username)
            return
        time.sleep(1)
        req = api.create_request()
        req.get_inventory()
        response = req.call()

        if type(response) is NotLoggedInException: #For some reason occasionally api.login lets fake ptc accounts slip through.. this will block em
            print "Failed to login the following account: {} (It may have been deleted)".format(username)
            return
            
        if response['status_code'] == 3:
            print('The following account is banned! {}'.format(username))
            if os.path.exists("banned.txt"):
                f = open('./banned.txt', 'a+b')
            else:
                f = open('./banned.txt', 'w+b')

            f.write("%s\n" % (username))

            f.close()
        else: print('Not banned...')


with open(str(sys.argv[1])) as f:
        credentials = [x.strip().split(':') for x in f.readlines()]

for username,password in credentials:
        try:
                check_account(username, password)
        except ServerSideRequestThrottlingException as e:
                print('Server side throttling, Waiting 10 seconds.')
                time.sleep(10)
                check_account(username, password)
        except NotLoggedInException as e1:
                print('Could not login, Waiting for 10 seconds')
                time.sleep(10)
                check_account(username, password)
