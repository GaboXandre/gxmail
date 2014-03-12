# GXMAIL v1.2.1

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
* text file attachment


# Usage

## Options
The following arguments are available
```
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
  
  -a ATTACHMENT, --attachment ATTACHMENT
                        Send file attachment.
                        
  -set, --settings      Access your profile settings. 
                        
```

## Interactive Mode

If called without arguments, *gxmail* will run in interactive mode.

## Batch mode 

    [-b FILE.TXT --batch FILE.TXT]
In batch mode, *gxmail* will read a list recepients from a text file.
*Notes:*
* The file must be plain text and contain one email per line
* *batch mode* is NOT compatible with *interactive mode*, you must provide arguments: to, subject, and message. Only the profile may be ommitted, in which case, the default profile is used.

*Spam is illegal, and it means you are evil if you use this software for that purpose.*

# Instalation Notes
## Dependencies
* python 2.7 o higher

## Install

* Uncompress the archive
* Copy *gxmail.py* to your desired directory. We recommend ```/usr/bin``` as it will be included in the PATH. 
* Run ```gxmail``` and it will complete the set up (see *first run* below for details)

```
cd path/to/gxmail
sudo cp gxmail.py /usr/bin/gxmail 	# copy file
sudo chmod +x /usr/bin/gxmail 		# make it excecutable
gxmail								# first run will complete setup.
```

# Profiles

## First Run
When you first run *gxmail.py* it will:
1. create **~/.gxmail** to store you profiles
2. prompt you to create your default profile:

```
 You don't have a profile set up yet. Let's do it now!
 Server -> smtp.mydomain.com
 Port -> 25
 Your email -> myemail@mydomain.com
 Your password -> myPa$$w0rd
 You are ready to send emails with your new profile!
```
## Profile Management
### Settings Mode
Running gxmail with argument **-set** or **--settings** will call a simple command line menu to manage your profiles.

```
 1 - View profiles                 
 2 - Add new profile                        
 3 - Delete existing profile          
 0 - Exit 
```


### Profile Files
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
* Add support for html
* Fixed bug on interactive profile selection

v1.1.3
* Adds *--version* flag
* Fix 'text/plain' Mime-type

v1.1.4
* Fixed bug with relative paths

v1.1.5
* Working on attachments

v1.1.6
* Now attachment is not options in interactive mode

v1.1.7
* Code cleanup

v1.1.8
* Settings Mode: manage your profiles from the command line. No more need to edit files manually.

v1.2.0
* small fixes

v1.2.1
* added support for Nano and Vim to write email content while using interactive mode.
