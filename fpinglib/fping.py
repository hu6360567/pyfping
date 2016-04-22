from subprocess import Popen, PIPE, STDOUT
from time import sleep
import re

FPING='/usr/bin/fping'

class Fping(object):

    def __init__(self,filename,timeout=500,count=3,interval=25):
        self.filename=filename
        self.timeout=timeout
        self.count=count
        self.interval=interval

    def __runcommand(self,command):
        process = Popen(command, stdout=PIPE,stderr=STDOUT)
        while True:
            result = process.stdout.readline().rstrip()
            if not result:
                break
            yield HostInfo(result)

    def checkStatus(self):
        cmd="%s -t %d -c %d -i %d -f %s -a" % (FPING,self.timeout,self.count,self.interval,self.filename)
        return self.__runcommand(cmd.split(' '))


class SingleFping(object):
    def __init__(self,filename,timeout=500,interval=25):
        self.filename=filename
        self.timeout=timeout
        self.interval=interval

    def __runcommand(self,command):
        process = Popen(command, stdout=PIPE,stderr=STDOUT)
        while True:
            host = process.stdout.readline().rstrip()
            if not host:
                break
            yield host

    def checkAlive(self):
        cmd="%s -t %d -i %d -f %s -a" % (FPING,self.timeout,self.interval,self.filename)
        return self.__runcommand(cmd.split(' '))

    def checkDead(self):
        cmd="%s -t %d -i %d -f %s -u" % (FPING,self.timeout,self.interval,self.filename)
        return self.__runcommand(cmd.split(' '))

class HostInfo(object):
    def __init__(self,result):
        # input string should be like
        # "baidu.com : xmt/rcv/%loss = 1/1/0%, min/avg/max = 113/113/113"
        fullmatch=re.match(r"(.*)[ ]*:[ ]*.*=[ ]*.*\/.*\/(.*)[ ]*%.*"
                           , result)
        if fullmatch:
            self.address=fullmatch.groups()[0]
            self.lossrate=fullmatch.groups()[1]