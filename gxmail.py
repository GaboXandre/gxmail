#!/usr/bin/env python
###############################################################
# LOGIC MODULE
###############################################################
import smtplib # for smtp support
import sys
import os
import argparse #for command line options/flags
import simplejson as json # to profiled stored in json files

# GLOBAL VARIABLES
AppInfo = { 'AppName' : 'gxmail',
			'Version' : '1.3.0',
			'Author' : 'Gabriel Godoy',
			'License' : 'GPL3',
			'copyright' : '2014 Gabriel Godoy'
			}

FileLocations = { 'ProfileDir' : os.path.expanduser('~/.gxmail/')}


# Command Line Flags and options
parser = argparse.ArgumentParser(description='%s is a simple text smpt client to send email from the command line. Very useful for scripts.' %(AppInfo['AppName']))
parser.add_argument('-p', '--profile', help='Select profile to be used.', required=False)
parser.add_argument('-to', help='Receipient. You may include several email addresses separating them with a comma. DO NOT use spaces', required=True)
parser.add_argument('-s', '--subject', help='subject line.', required=True)
parser.add_argument('-m', '--message', help='Import email body from text file.', required=False)
#parser.parse_args(file['out.txt'])
parser.add_argument('-i', '--interactive', help='Launch compose prompt.', required=False, action="store_true")
args = parser.parse_args()

# PROFILE MANAGEMENT SECTION
def create_profile(defprofile):
	default_file = FileLocations['ProfileDir']+'/default'
	default = open(default_file, 'w')
		
	default.write(json.dumps(defprofile))
	default.close()
	res = 'You are ready to send emails with your new profile!'
	return res

def additional_profiles():
	print '-'*80
	print "So you wan't to add a new profile? Let's do it!"
	print '-'*80
	name = raw_input('Name your profile -> ')
	server = raw_input('Server -> ')
	port = raw_input('Port -> ')
	email = raw_input('Your email -> ')
	password = raw_input('Your password -> ')

	profile = []
	profile.append(name)
	profile.append(server)
	profile.append(port)
	profile.append(email)
	profile.append(password)
	
	create_profile(profile)

def test_profiles():
	f = []
	for (dirpath, dirnames, filenames) in os.walk(FileLocations['ProfileDir']):
		f.extend(filenames)
		break
	length = len(f)

	if length == 0:
		print '-'*80
		print "You don't have a profile set up yet. Let's do it now!"
		print '-'*80
		server = raw_input('Server -> ')
		port = raw_input('Port -> ')
		email = raw_input('Your email -> ')
		password = raw_input('Your password -> ')
	
		defprofile = ['default']
		defprofile.append(server)
		defprofile.append(port)
		defprofile.append(email)
		defprofile.append(password)
		
		setup = create_profile(defprofile)
		
		
	else:
		send_mail()

#Main Program
def select_profile():
	profile = str(args.profile)
	if profile == 'None':
		profile_name = 'default'
		#return profile
	else:
		profile_name = str(args.profile)
		#return profile
	profile_location = FileLocations['ProfileDir']+profile_name
	# load profile info
	myfile = open(profile_location)
	myfile2 = myfile.read()
	profile = json.loads(myfile2)
	return profile
	


def initialize_smtp_server(profile):
    server = profile[1]
    port = profile[2]
    email = profile[3]
    password = profile[4]
    smtpserver = smtplib.SMTP(server, port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(email, password)
    return smtpserver

def send_mail():
    profile = select_profile()
    to_email = args.to
    from_email = profile[3]
    subject = args.subject
    
    # parse message from text file
    header = "To:%s\nFrom:%s\nSubject:%s \n" % (to_email, from_email, subject)
	
	# extract message content from file
    file_name = args.message
    the_file = open(file_name)
    msg = the_file.read()
    the_file.close()

    content = header + "\n" + msg
    smtpserver = initialize_smtp_server(profile)
    smtpserver.sendmail(from_email, to_email, content)
    smtpserver.close()
    
    
print '='*80
print 'gxmail - version %s' %(AppInfo['Version'])
print '='*80
test_profiles()
