#! /usr/bin/env python

import web
import sys
import logging
# import time
from datetime import datetime
import asterisk
import asterisk.manager
import asterisk.config

logging.basicConfig(
    filename='log/c2c.log',
    level=logging.DEBUG,
    format='%(asctime)s]:%(process)d:%(levelname)s : %(funcName)s %(message)s')

logging.debug('INIT %s', datetime.now())

# Note that we eventually want to make this more of an ambiguous handler,
# accepting a variety of variables

#def call_handler(action, endpt, caller_id, destination):
    ## This function is the call handler. it walks a call from inception to
    ## termination.
    #status = ast.status()
    #logging.debug('Ast status: %s' % status)
    #ast.dial(action, endpt, caller_id, destination)
    #pass


urls = (
    '/c2c', 'Request_handler'
    )
app = web.application(urls, globals())

logging.debug('Just below app')

class Request_handler(object):
    # Class designeed for HTTP interaction with applications seeking to
    # to use this binary as an application gateway.
    def __init__(self):
        logging.debug('Init Request_handler instance')

    def GET(self):
        logging.debug('GET has been received!')
        data = web.input()
        # action = data.action
        action = data.action
        # endpt = data.endpt
        tech = 'SIP/'
        channel = tech + data.endpt
        # caller_id = data.callerid
        caller_id = data.callerid
        # destination = data.destination
        destination = data.destination
        logging.debug('Setting up the call')
        call = AMI()
        call.dial(
            channel,
            caller_id,
            destination
            )


class AMI(object):
    # Class designed for interacting wtih the Asterisk AMI.

    def __init__(self):
        logging.debug('AMI Initializer fired!')
        self.conf()
        logging.debug('INIT')
    def handle_shutdown(self, event, manager):
        logging.debug("Received shutdown event")
        manager.close
        # we could analize the event and reconnect here

    def handle_event(self, event, manager):
        logging.debug('Received event: %s' % event.name)

    def conf(self):
        # load and parse the config file
        logging.debug('We have reached the configurator')
        try:
            config = asterisk.config.Config(
                '/etc/asterisk/manager_custom.conf')
        except asterisk.config.ParseError, (line, reason):
            logging.debug('Parse Error line: %s: %s' % (line, reason))
            sys.exit(1)
        except IOError, reason:
            logging.debug('Error opening file: %s' % reason)
            sys.exit(1)

        # Log our parsed output
        for category in config.categories:
            if category.name != 'general':
                self.user = category.name
                # DEBUG: This section is strictly for debugging.
                self.host = '74.222.51.243'
                # user = 'c2c'
                self.secret = 'c2c'
                # self.host = host
                # self.user = user
                # self.secret = secret
                logging.debug('User: %s' % self.user)
                # logging.debug('Pass: %s' % self.secret)
                # End debug section.
            else:
                logging.debug('Category name: %s' % category.name)

        # for (item.name == 'secret') in category.items:
        #    secret = item.value
        #    self.secret = item.value

    def dial(self, channel, caller_id, destination):
        manager = asterisk.manager.Manager()
        manager.connect(self.host)
        manager.login(self.user, self.secret)
        logging.debug('Calling originate')
        context = 'from-internal'
        priority = '1'
        timeout = '30000'
        manager.originate(
            channel ,
            destination ,
            context = context ,
            priority = priority ,
            timeout = timeout ,
            caller_id = caller_id,
            )
        manager.logoff()

        pass

    def status(self):
        # Intended to get a status report from the server, to verify that
        # we are still connected.
        manager = asterisk.manager.Manager()
        response = manager.status
        logging.debug('Status: %s' % response)


if __name__ == "__main__":
    try:
        logging.debug('Start of the main loop')
        # Create the first instance of AMI.
        # This allows us to start the loop for the HTTP listener. Events are
        # triggered by applications here.
        app.run()
        logging.debug('Just after app.run')
    except (KeyboardInterrupt, SystemExit):
        logging.warning('EXCEPTION CAUGHT, Exiting.')
