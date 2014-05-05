#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, json

def createDaemon():
  """ 
      This function create a service/Daemon that will execute a det. task
  """
  jsonfile = open('settings.json')
  settings = json.load(jsonfile)
  jsonfile.close()

  try:
    pidfile = open(settings['pidfile'])
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
      with open(settings['pidfile'], 'w') as pidfile:
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
  file = open('/tmp/tarefa.log', 'w')

  # Start the write
  while True:
    print >> file, time.ctime()
    file.flush()
    time.sleep(2)

  # Close the file
  file.close()

if __name__ == '__main__':

  # Create the Daemon
  createDaemon()
