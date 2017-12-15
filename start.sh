# start all servers
python2 DirectoryServer.py &
python2 LockServer.py &
python2 ReplicationServer.py 8003 &
python2 ReplicationServer.py 8009 &
