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


# Note that we eventually want to make this more of an ambiguous handler,
# accepting a variety of variables

def call_handler(action, endpt, callerid, destination):
    # This function is the call handler. it walks a call from inception to
    # termination.
    status = ast.status()
    logging.debug('Ast status: %s' % status)
    ast.dial(action, endpt, callerid, destination)
    pass


urls = (
    '/c2c', 'Request_handler'
    )

app = web.application(urls, globals())

logging.debug('Just below app')

class Request_handler():
    # Class designeed for HTTP interaction with applications seeking to
    # to use this binary as an application gateway.
    def GET(self):
        logging.debug('GET has been received!')
        data = web.input()
        logging.debug(data.action)
        logging.debug(data.endpt)
        logging.debug(data.callerid)
        logging.debug(data.destination)
        # call = AMI()
        # call.dial(
        #    data.endpt,
        #    data.callerid,
        #    data.destination)
        action = data.action
        endpt = data.endpt
        callerid = data.callerid
        destination = data.destination
        print(data.action, data.endpt, data.callerid, data.destination)
        call = AMI()
        call.dial(
            data.endpt,
            data.callerid,
            data.destination)


class AMI(object):
    # Class designed for interacting wtih the Asterisk AMI.

    def __init__(self):
        logging.debug('AMI Initializer fired!')
        self.conf()
        logging.debug('self.conf set.')
        self.auth()
        logging.debug('self.auth set')

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
                self.host = '72.216.234.100'
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

    #def dial(self, endpt, cid, destination):
        #logging.debug('Dial has been fired!')
        ## auth = self.auth()
        #if (self.status == 'ok'):
            #logging.debug('Status 2: %s' % self.status)
            #manager = asterisk.manager.Manager()
            #context = 'UA'
            ## Just for debugging.
            #endpt2 = 'SIP/4005'
            #d = '3033786762'
            #priority = '1'
            #timeout = '3000'
            #caller_id = '1112223333'
            #manager.connect(self.host)
            #response = manager.status
            #manager.originate(
                #endpt2 ,
                #destination ,
                #context = 'UA' ,
                #priority = '1' ,
                #timeout = '30000' ,
                #caller_id = '1112223333' ,
                #)
            #print(endpt2, d, context, priority, timeout, caller_id)
        #else:
            #logging.debug('Not OK %s' % self.status)
        ## we authenticate and everything is fine - we need a return system
            ## for auth.

        #pass

    def auth(self):
        logging.debug('We have fired the authenticator!')
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
            logging.debug('Response: %s ' % response)
            logging.debug(manager.status())
            endpt2 = 'SIP/4005'
            destination = '3033786762'
            manager.originate(
                endpt2 ,
                destination ,
                context = 'UA' ,
                priority = '1' ,
                timeout = '30000' ,
                caller_id = '1112223333' ,
                )

            test = manager.sippeers()
            logging.debug('Sippeers: %s' % test)
            # This is the supposed return value.
            self.status = 'ok'
            logging.debug(self.status)

        except asterisk.manager.ManagerSocketException, (errno, reason):
            logging.debug('Error connecting to the manager: %s' % reason)
            sys.exit(1)

        except asterisk.manager.ManagerAuthException, reason:
            logging.debug('Error logging in to the manager: %s' % reason)
            sys.exit(1)

        except asterisk.manager.ManagerException, reason:
            logging.debug('Error: %s' % reason)
            sys.exit(1)

    def status(self):
        # Intended to get a status report from the server, to verify that
        # we are still connected.
        manager = asterisk.manager.Manager()
        response = manager.status
        logging.debug('Status: %s' % response)

    def logoff(self):
        # Logs off the manager connection.
        manager = asterisk.manager.Manager()
        manager.logoff()
        logging.debug('Logging off')


if __name__ == "__main__":
    try:
        logging.debug('INIT %s', datetime.now())
        # Create the first instance of AMI.
        ast = AMI()
        logging.debug('ast has been created.')
        # This allows us to start the loop for the HTTP listener. Events are
        # triggered by applications here.
        app.run()
        logging.debug('Just below run')
    except (KeyboardInterrupt, SystemExit):
        logging.warning('EXCEPTION CAUGHT, Exiting.')
