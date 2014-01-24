# GXMAIL v1.1.1 

*gxmail* is a simple smtp client designed to send emails from the linux command line.
It is particularly useful to use with bash scripts. 
*gxmail* supports multiple profiles (email accounts)

# Features
* smtp
* multiple profiles
* multiple recepients
* load email body from file

# Options
  -h, --help            show this help message and exit
  
  -p PROFILE, --profile PROFILE
                        Select profile to be used.
                        
  -to TO                Receipient. You may include several email addresses
                        separating them with a comma. DO NOT use spaces
                        
  -s SUBJECT, --subject SUBJECT
                        subject line.
                        
  -m MESSAGE, --message MESSAGE
                        Import email body from text file.
  -i,         --interactive
  						Interactive prompt. 
                        

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
v1.1.0 Adds interactive mode
v1.1.1 Adds batch mode, reads recepients form text file
