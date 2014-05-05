#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, json, urllib2
_SETTINGS = dict()

def createDaemon():
  global _SETTINGS
  """ 
      This function create a service/Daemon that will execute a det. task
  """
  jsonfile = open('settings.json')
  _SETTINGS = json.load(jsonfile)
  jsonfile.close()
  print json.dumps(_SETTINGS)
  print _SETTINGS['interval']

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
    _new_ = urllib2.urlopen("http://curlmyip.com/").read().strip()
    print >> file, time.ctime() + ' ip: ' + _new_
    print >> file, 'next update check in %d seconds.' % _SETTINGS['interval']
    file.flush()    
    time.sleep(_SETTINGS['interval'])

  # Close the file
  file.close()

if __name__ == '__main__':

  # Create the Daemon
  createDaemon()
