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
    filename='/var/log/asterisk/c2c.log',
    level=logging.DEBUG,
    format='%(asctime)s]:%(process)d:%(levelname)s : %(funcName)s %(message)s')

urls = (
    '/c2c', 'Request_handler'
    )

app = web.application(urls, globals())

server_url = 'http://localhost:8080'


class Request_handler():
    # Class designeed for HTTP interaction with applications seeking to
    # to use this binary as an application gateway.
    def GET(self):
        logging.debug('GET called')
        data = web.input()
        logging.debug(data.extension)
        logging.debug(data.callerid)
        logging.debug(data.phone)
        call = AMI()
        call.dial(
            data.extension,
            data.callerid,
            data.phone)


class AMI(object):
    # Class designed for interacting wtih the Asterisk AMI.

    def __init__(self):
        logging.debug('We are at AMI.__init__')
        self.conf()
        logging.debug('self.conf set.')

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
                # host = 'localhost'
                # user = 'c2c'
                # secret = 'c2c'
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

    def dial(self, ext, cid, phone_num):
        logging.debug('DIAL')
        pass

    def auth(self):
        logging.debug('AMI.auth')
        manager = asterisk.manager.Manager()
        # connect to the manager
        try:
            # manager.connect('host')
            manager.connect(self.host)
            manager.login(self.user, self.secret)

            # register some callbacks
            # shutdown
            manager.register_event('Shutdown', self.handle_shutdown)
            # catch all
            manager.register_event('*', self.handle_event)

            # get a status report
            response = manager.status()
            logging.debug(response)
            manager.logoff()
            logging.debug('Logging off')

        except asterisk.manager.ManagerSocketException, (errno, reason):
            logging.debug('Error connecting to the manager: %s' % reason)
            sys.exit(1)

        except asterisk.manager.ManagerAuthException, reason:
            logging.debug('Error logging in to the manager: %s' % reason)
            sys.exit(1)

        except asterisk.manager.ManagerException, reason:
            logging.debug('Error: %s' % reason)
            sys.exit(1)


if __name__ == "__main__":
    try:
        logging.debug('INIT %s', datetime.now())
        # Create the first instance of AMI.
        ast = AMI()
        logging.debug('ast has been created.')
        logging.debug('Passed the calls')
        # This allows us to start the loop for the HTTP listener. Events are
        # triggered by applications here.
        app.run()
    except (KeyboardInterrupt, SystemExit):
        logging.warning('EXCEPTION CAUGHT, Exiting.')
