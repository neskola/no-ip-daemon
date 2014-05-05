#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, json, urllib2, base64
_SETTINGS = dict()

def createDaemon():
  global _SETTINGS
  """ 
      This function create a service/Daemon that will execute a det. task
  """
  jsonfile = open('settings.json')
  _SETTINGS = json.load(jsonfile)
  jsonfile.close()
  #print json.dumps(_SETTINGS)
 
  try:
    pidfile = open(_SETTINGS['pidfile'])
    print 'Error: pid file already exists'
    pidfile.close()
    os._exit(1)
  except IOError, error:
    print 'Forking new process'

  try:
    # Store the Fork PID

    pid = os.fork()

    if pid > 0:
      print 'PID: %d' % pid
      with open(_SETTINGS['pidfile'], 'w') as pidfile:
        pidfile.write(str(pid))
        pidfile.close()
      os._exit(0)

  except OSError, error:
    print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
    os._exit(1)

  doTask()

def doTask():
  """ 
      This function create a task that will be a daemon
  """
  # Open the file in write mode
  file = open(_SETTINGS['log'], 'w')

  # Start the write
  while True:
    _new_ = urllib2.urlopen(_SETTINGS['ipresolve']).read().strip()
    _url_ = _SETTINGS['updateurl']
    
    print >> file, time.ctime() + ' ip: ' + _new_
    print >> file, 'next update check in %d seconds.' % _SETTINGS['interval']

    # Update current public ip
    _url_called_ = _url_.format(hostname=_SETTINGS['hostname'], ip=_new_)
    _user_data_ = "Basic " + (_SETTINGS['username'] + ":" + _SETTINGS['password']).encode("base64").rstrip()
    
    print >> file, _url_called_ + " " + _user_data_

    req = urllib2.Request(_url_)
    req.add_header("Authorization", _user_data_)
    
    try:
      res = urllib2.urlopen(req)
      print >> file, 'response is ' + res.read()
      print >> file, '... Succeed'
    except urllib2.HTTPError:
      print >> file, " authentication error" 
            
    
    file.flush()    
    time.sleep(_SETTINGS['interval'])

  # Close the file
  file.close()

if __name__ == '__main__':

  # Create the Daemon
  createDaemon()



