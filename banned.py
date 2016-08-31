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
import argparse
import re

def parse_arguments(args):
    """Parse the command line arguments for the console commands.
    Args:
      args (List[str]): List of string arguments to be parsed.
    Returns:
      Namespace: Namespace with the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Pokemon Trainer Club Banned Account Checker'
    )
    parser.add_argument(
        '-f', '--file', type=str, default=None, required=True,
        help='File of accounts to check (formatted username:password).'
    )
    parser.add_argument(
        '-l', '--location', type=str, default="40.7127837 -74.005941", required=False,
        help='Location to use when checking if the accounts are banned.'
    )
    return parser.parse_args(args)

def check_account(username, password, location):
        api = PGoApi()
        auth = 'ptc'
        api.set_position(location[0], location[1], 0.0)
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
            appendFile(username)
            return

        if response['status_code'] == 3:
            print('The following account is banned! {}'.format(username))
            appendFile(username)
        else: print('{} is not banned...'.format(username))

def appendFile(username):
    if os.path.exists("banned.txt"):
        f = open('./banned.txt', 'a+b')
    else:
        f = open('./banned.txt', 'w+b')

    f.write("%s\n" % (username))

    f.close()

def entry():
    args = parse_arguments(sys.argv[1:])

    prog = re.compile("^(\-?\d+\.\d+),?\s?(\-?\d+\.\d+)$")
    res = prog.match(args.location)
    if res:
        print('Using the following coordinates: {}'.format(args.location))
        position = (float(res.group(1)), float(res.group(2)), 0)
    else:
        print('Failed to parse the supplied coordinates ({}). Please try again.'.format(args.location))
        return

    with open(str(args.file)) as f:
            credentials = [x.strip().split(':') for x in f.readlines()]

    for username,password in credentials:
            try:
                    check_account(username, password, position)
            except ServerSideRequestThrottlingException as e:
                    print('Server side throttling, Waiting 10 seconds.')
                    time.sleep(10)
                    check_account(username, password, position)
            except NotLoggedInException as e1:
                    print('Could not login, Waiting for 10 seconds')
                    time.sleep(10)
                    check_account(username, password, position)

entry()
