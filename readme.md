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
Required dependencies are listed in the requirement.txt file in this directory. All required dependencies should be installed automatically by setup.py. Asterisk has some requirements as well, such as dialplan configuration and conf files. 

#### Asterisk Requirements
```asterisk/conf/c2c.conf``` has been created and needs to be installed on the client machine. In this case the phone system is using FreePBX, so extensions_custom.conf has been made that has an ```include``` statement that includes ```c2c.conf```. The dialplan there will then initiate the call based on the variables that were recieved via the Asterisk Manager Interface from a connection initiated by c2c.py. 

#### Caesar Requirements
A specific build of Caesar has been created using the form customerNEW, which has a button that activates an IE control. The IE control sends an HTTP post to this application that contains variables used for setting up the call.  

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

