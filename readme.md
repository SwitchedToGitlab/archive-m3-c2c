# Click2Call Application
## Table of Contents
- [Installation](#Installation)
    - [Basic Requirements](#basic-requirements)
    - [Virtualenv](#virtualenv)
    - [Supervisorctl](#supervisorctl)
    - [Configuration](#configuration)
- [Usage](#usage)
    - [Starting and Stopping](#starting-and-stopping)
    - [User Experience](#user-experience-what-to-expect)
- [Troubleshooting and Logging ](#Troubleshooting-and-Logging)
- [Errors and Bugs](#errors-and-bugs)
- [License](#license)

## Introduction
## Installation
    ### Requirements
## Usage
    ### Starting and Stopping
    ### User Experience: What to Expect
## Troubleshooting and Logging
    <!--- TODO: Flesh this out a little more --->
    Check the supervisord logs on the system 
## Errors and Bugs
    There may be errors and bugs in this software, as with all software. Please report any issues to support@haikuengineering.com
## License
    See the included UNLICENSE file in the current directory. 



This python server is designed to respond to GET requests made by an
application and take those parameters passed to it in the GET request and use
those to create an AMI connection with Asterisk. 

This application will begin by initiating a call.

The application uses python 2.x, with modules web.py and pyst2 third party
modules.

The application also needs an AMI user created with unlimited permissions.
This must be created in /etc/asterisk/manager_custom.conf for FreePBX, as the
application parses this file and uses the first entry that it finds. We can
customize this further if needed, such as using a discreet file for this
appliocation's manager user.

