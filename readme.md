This python server is designed to respond to GET requests made by an
application and take those parameters passed to it in the GET request and use
those to create an AMI connection with Asterisk. 

This application will being by initiating a call.

The application uses python 2.x, with modules web.py and pyst2 third party
modules.

The application also needs an AMI user created with unlimited permissions.
This must be created in /etc/asterisk/manager_custom.conf for FreePBX, as the
application parses this file and uses the first entry that it finds. We can
customize this further if needed, such as using a discreet file for this
appliocation's manager user.

