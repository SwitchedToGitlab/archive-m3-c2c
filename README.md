# Click2Call Application
## Table of Contents
- [Installation](#Installation)
    - [Requirements](#requirements)
        - [Host Requirements](#host-requirements)
        - [Asterisk Requirements](#asterisk-requirements)
    - [Virtualenv](#virtualenv)
    - [Supervisord](#supervisord)
    - [Configuration](#configuration)
- [Usage](#usage)
    - [Starting and Stopping](#starting-and-stopping)
    - [User Experience](#user-experience-what-to-expect)
- [Troubleshooting and Logging ](#Troubleshooting-and-Logging)
- [Errors and Bugs](#errors-and-bugs)
- [License](#license)

****

## Introduction
    
This python server is designed to respond to GET requests made by an
application and take those parameters passed to it in the GET request and use
those to create an AMI connection with Asterisk. 
## Installation
### Requirements
#### Host Requirements
##### Python    
The application uses python 2.x, with modules web.py and pyst2 third party
modules. See requirements.txt for more information.
##### Virtualenv
Virtualenv must be installed via the system package manager and kept up to 
date.
##### Supervisord
Supervisord must be installed via the system package manage and kept up to 
date. See the conf directory for supervisord configuration options. 
##### Configuration
#### Asterisk Requirements
##### AMI 
The application also needs an AMI user created with unlimited permissions.
This must be created in /etc/asterisk/manager_custom.conf for FreePBX, as the
application parses this file and uses the first entry that it finds. We can
customize this further if needed, such as using a discreet file for this
appliocation's manager user.
##### Dialplan
For Freepbx systems, add the extensions_override.conf file's contents to the 
file on the host system. 

## Usage
### Starting and Stopping
 
### User Experience: What to Expect
This application will begin by initiating a call.
## Troubleshooting and Logging
Check the supervisord logs on the system 
## Errors and Bugs
There may be errors and bugs in this software, as with all software. Please report 
any issues to support@haikuengineering.com
## License
See the included UNLICENSE file in the current directory. 