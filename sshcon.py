#!/usr/bin/python
import sys, os
import re

DIR = os.path.dirname(os.path.abspath(__file__))
# DIR = '/home/avi/bin/'
sshargs = '-X -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'

def set_color (string, color):
    colors = {"default": 0, "red": 31, "green": 32, "yellow": 33, "blue": 34,
              "magenta": 35, "cyan": 36, "white": 37, "black": 39}  # 33[%colors%m

    color_string = "\033[%dm\033[1m" % colors[color]
    return color_string + string + '\033[0m'

def collectConn():
    groups = {}
    gname = 'global'
    groups[gname] = []
    with open(os.path.join(DIR, '.servers'), 'r') as f:
        for line in f.readlines():
            if line.strip() and line.startswith('#'):
                continue
            match = re.match(r'^\[(\w+)\]$', line.strip())
            if match:
                gname = match.groups()[0]
                groups[gname] = []
                continue
            if line.strip() and not line.startswith('#'):
                line = line.replace(' ', '').split(',')
                conn = line[0]
                if not conn.split('@')[0]:
                    conn = os.getenv('USERNAME') + line[0]
                line = [conn, line[1].strip()]
                groups[gname].append(line)
    if not groups['global']:
        groups.pop('global')
    return groups

def colorConnList(serversDict):
    newServersList = []
    colors = ['red', 'white', 'cyan', 'magenta', 'green', 'yellow']
    colorIndex = 0
    for grp, serversList in serversDict.iteritems():
        if colorIndex >= len(colors):
            colorIndex = 0
        for serv in serversList:
            newServersList.append(serv)
            msg = '%s - %s' % (newServersList.index(serv) + 1, serv[1])
            print set_color(msg, colors[colorIndex])
        colorIndex += 1
    return newServersList

def getServerData(server, serversList):
    for serv in serversList:
        if server in serv:
            return serv
    return 'root:%s' % server

def buildCommand(data):
    cmd = 'ssh %s %s'
    cmd = cmd % (sshargs, data[0])
    return cmd

def usage(servers):
    for grp, lconn in servers.iteritems():
        for conn in lconn:
            print conn[1]
    sys.exit(0)


if __name__ == '__main__':
    serversDict = collectConn()


    dest_info = ''
    serversList = []

    if len(sys.argv) > 1:
        if '-m' in sys.argv:
            usage(serversDict)
        dest_info = getServerData(sys.argv[1], serversList)
    else:
        serversList = colorConnList(serversDict)
        number = input("Enter Server number:")
        if number <= 0:
            print 'Negetive or Zero numbers are not supported.'
            sys.exit(1)
        number -= 1
        dest_info = serversList[number]

    os.system(buildCommand(dest_info))
