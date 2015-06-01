#! /usr/bin/env python

import web
import sys
import logging
from datetime import datetime
import asterisk
import asterisk.manager
import asterisk.config

logging.basicConfig(
    filename='/var/log/c2c/debug.log',
    level=logging.DEBUG,
    format='%(asctime)s]:%(process)d:%(levelname)s : %(funcName)s %(message)s')

logging.debug('INIT %s', datetime.now())

# Note that we eventually want to make this more of an ambiguous handler,
# accepting a variety of variables

urls = (
    '/c2c', 'Request_handler'
    )
app = web.application(urls, globals())

class Request_handler(object):
    # Class designeed for HTTP interaction with applications seeking to
    # to use this binary as an application gateway.
    def __init__(self):
        logging.debug('Init Request_handler instance')

    # This method is fired when the webserver receives a GET event,
    # then creates the call. Eventually this logic will be passed off
    # somewhere else, but for now for the sake of simplicity it's here.
    def GET(self):
        logging.debug('GET received!')
        data = web.input()
        call = AMI()
        call.dial(
            data.endpt,
            data.callerid,
            data.destination
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
                self.host = 'localhost'
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



    def dial(self, endpt, caller_id, destination):
        logging.debug('INIT')
        manager = asterisk.manager.Manager()
        manager.connect(self.host)
        manager.login(self.user, self.secret)
        logging.debug(self.status)
        tech = 'PJSIP/'
        channel = tech + endpt
        logging.debug(channel)
        logging.debug('Calling originate')
        context = 'c2c'
        priority = '1'
        timeout = '30000'
        modified_cid = 'Caesar <' + destination + '>'
        logging.debug(modified_cid)
        manager.originate(
            channel ,
            destination ,
            context = context ,
            priority = priority ,
            timeout = timeout ,
            caller_id = modified_cid,
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
        logging.debug('INIT')
        app.run()
    except (KeyboardInterrupt, SystemExit):
        logging.warning('EXCEPTION CAUGHT, Exiting.')
