#!/usr/bin/python
import sys, os
import re

DIR = os.path.dirname(os.path.abspath(__file__))
sshargs = '-X -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

def set_color (string, color):
    colors = {"default": 0, "red": 31, "green": 32, "yellow": 33, "blue": 34,
              "magenta": 35, "cyan": 36, "white": 37, "black": 39} #33[%colors%m

    color_string = "\033[%dm\033[1m" % colors[color]
    return color_string + string + '\033[0m'

def collectConn():
    groups = {}
    gname = 'global'
    groups[gname] = []
    with open(os.path.join(DIR,'.servers'), 'r') as f:
        for line in f.readlines():
            if line.strip() and line.startswith('#'):
                continue
            match = re.match(r'^\[(\w+)\]$', line.strip())
            if match:
                gname = match.groups()[0]
                groups[gname] = []
                continue
            if line.strip() and not line.startswith('#'):
                groups[gname].append(line)
    if not groups['global']:
        groups.pop('global')
    return groups

def colorConnList():
    newServersList = []
    serversDict = collectConn()
    colors= ['red', 'white', 'cyan', 'magenta', 'green', 'yellow']
    colorIndex = 0
    for grp, serversList in serversDict.iteritems():
        if colorIndex >= len(colors):
            colorIndex = 0
        for serv in serversList:
            try:
                l = serv.split(':')[1].strip()
            except IndexError:
                l = serv.strip()
            newServersList.append(serv)
            msg = '%s - %s' % (newServersList.index(serv)+1, l)
            print set_color(msg, colors[colorIndex])
        colorIndex += 1
    return newServersList

def listConn():
    newServersList = []
    serversDict = collectConn()
    for grp, serversList in serversDict.iteritems():
        for serv in serversList:
            try:
                serv.split(':')[1].strip()
            except IndexError:
                serv.strip()
            newServersList.append(serv)
    return newServersList

def getServerData(server, serversList):
    for serv in serversList:
        if server in serv:
            return serv
    return 'root:%s' % server

def buildCommand(data):
    cmd = 'ssh %s %s'
    try:
        target = data.split(':')[1].strip()
        user = data.split(':')[0].strip()
        cmd += ' -l %s' % user
    except IndexError:
        target = data.strip()

    cmd = cmd % (sshargs, target)
    return cmd

def usage(servers):
    for server in servers:
        server = server.strip()
        try:
            print server.split(':')[1]
        except IndexError:
            print server
    sys.exit(0)

if __name__ == '__main__':
    dest_info = ''
    serversList = []

    if len(sys.argv) > 1:
        serversList = listConn()
        if '-m' in sys.argv:
            usage(serversList)
        dest_info = getServerData(sys.argv[1], serversList)
    else:
        serversList = colorConnList()
        number = input("Enter Server number:")
        if number <= 0:
            print 'Negetive or Zero numbers are not supported.'
            sys.exit(1)
        number -= 1
        dest_info = serversList[number]

    os.system(buildCommand(dest_info))
