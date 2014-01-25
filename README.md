# GXMAIL v1.1.3

*gxmail* is a simple smtp client designed to send emails from the linux command line.
It is particularly useful to use with bash scripts. 
*gxmail* supports multiple profiles (email accounts)

# Features
* smtp
* multiple profiles
* load email body from file
* html support
* batch mode to enable mailing lists
* interactive mode


# Usage

## Options
The following arguments are available

  -h, --help            show this help message and exit

  -p PROFILE, --profile PROFILE
                        Select profile to be used.

  -to TO                Receipient. You may include several email addresses
                        separating them with a comma. DO NOT use spaces

  -s SUBJECT, --subject SUBJECT
                        subject line.

  -m MESSAGE, --message MESSAGE
                        Import email body from text file.

  -b BATCH, --batch BATCH
                        Batch mode: get recepients from a text file.

  -html, --html         HTML mode: send html formated content.

  -v, --version         Prints version and exits program.


## Interactive Mode

If called without arguments, *gxmail* will run in interactive mode.

## Batch mode 

**[-b FILE.TXT --batch FILE.TXT]**
In batch mode, *gxmail* will read a list recepients from a text file.
*Notes:*
* The file must be plain text and contain one email per line
* *batch mode* is NOT compatible with *interactive mode*, you must provide arguments: to, subject, and message. Only the profile may be ommitted, in which case, the default profile is used.

*Spam is illegal, and it means you are evil if you use this software for that purpose.*

# Instalation Notes
## Dependencies
* python 2.7 o higher

## Install

* Copy *gxmail.py* to your desired application.
* *gxmail* will store profiles in *~/.gxmail*, you will need to create this directory manually. And keep it empty, do **NOT** place *gxmail.py* inside it.
 mkdir ~/.gxmail
* Make sure *gxmail.py* is executable
> chmod +x <path>/gxmail.py
* Run the script, you will be prompted to create your default profile.
 ./gxmail.py

# Profiles

## First Run
When you first run *gxmail.py* it will prompt you to create your default profile:

 You don't have a profile set up yet. Let's do it now!
 Server -> smtp.mydomain.com
 Port -> 25
 Your email -> myemail@mydomain.com
 Your password -> myPa$$w0rd
 You are ready to send emails with your new profile!

## Profile Management
Each profile is stored as a text file inside *~/.gxmail*
You can simply delete each file to remove a profile.
It is also posible to edit them with your favorite text editor, just remember to keep the structure:

 ["Profilename", "server", "port", "email", "password"]

Example:

 ["default", "smtp.mydomain.com", "25", "myemail@mydomain.com", "myPa$$w0rd"]

# License

This software is realeased under GPL3.

# Contact

email: gabo.xandre@gmail.com

# ChangeLog
v1.1.0 
* Add interactive mode

v1.1.1 
* Add batch mode, read recepients form text file

v1.1.2 
* Add sopport for html
* Fixed bug on interactive profile selection

v1.1.3
* Adds *--version* flag
* Fix 'text/plain' Mime-type
