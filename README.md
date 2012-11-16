sshcon:
An application that makes ssh connections faster and easier when handling multiple servers list.

1. create a menu of servers and give the option to input index and connect to server.
2. autocomplition of server name while running sshcon.

INSTALL:
1. move etc/bash_completion.d/sshcon to /etc/bash_completion.d/
2. add '. /etc/bash_completion.d/sshcon' to ~/.bashrc
3. move sshcon.py to ~/bin or any other executable path.
4. create link to sshcon: ln -s ~/bin/sshcon.py ~/bin/sshcon
5. add .servers to that path as well

.servers configurations:
1. groups: servers file can be devided to groups by [GROUP_NAME]

[test_group]
server.address.name
root:second.server.address.name
[test_groupo2]
root:.....


2. as written above, servers address can have prefix of the user we would like to connect with and than ':' delimiter.
3. no username prefix will actually connect via the loged in user.
4. each group will have his own color

USAGE:
1. $ sshcon
   will display a list of servers collected from '.servers' file.
2. $ sshcom <TAB>
   will give autocomplition of servers from '.servers' file

