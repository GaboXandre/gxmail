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
			'Version' : '1.1.2',
			'Author' : 'Gabriel Godoy',
			'License' : 'GPL3',
			'copyright' : '2014 Gabriel Godoy'
			}

FileLocations = { 'ProfileDir' : os.path.expanduser('~/.gxmail/')}


# Command Line Flags and options
parser = argparse.ArgumentParser(description='%s is a simple text smpt client to send email from the command line. Very useful for scripts.' %(AppInfo['AppName']))
parser.add_argument('-p', '--profile', help='Select profile to be used.', required=False)
parser.add_argument('-to', help='Receipient. You may include several email addresses separating them with a comma. DO NOT use spaces', required=False)
parser.add_argument('-s', '--subject', help='subject line.', required=False)
parser.add_argument('-m', '--message', help='Import email body from text file.', required=False)
parser.add_argument('-b', '--batch', help='Batch mode: get recepients from a text file.', required=False)
parser.add_argument('-html', '--html', help='HTML mode: send html formated content.', required=False, action="store_true")
args = parser.parse_args()



# PROFILE MANAGEMENT SECTION
def create_profile(defprofile):
	default_file = FileLocations['ProfileDir']+'/default'
	default = open(default_file, 'w')
		
	default.write(json.dumps(defprofile))
	default.close()
	res = 'You are ready to send emails with your new profile!'
	return res

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
		test_options()


def test_options():
	values = [args.profile, args.to, args.subject, args.message, 'text']
	p = select_profile(values[0])
	t = str(args.to)
	s = str(args.subject)
	m = str(args.message)
	b = str(args.batch)
	h = args.html
	
	int_mode = 'off'
	if h is True:
		values[4] = 'text/html'
	else:
		values[4] = 'text'
	
	if t == 'None':
		values[1] = 0
		int_mode = 'on'
	if s == 'None':
		values[2] = 0
		int_mode = 'on'
	if m == 'None':
		values[3] = 'empty'
		int_mode = 'on'

	if b != 'None':
		values = [p, args.to, args.subject, args.message, values[4]]
		int_mode = 'off'
		batch_mode(values)
		
	if int_mode == 'on':
		interactive_mode(values)
	else:
		values = [p, args.to, args.subject, args.message, values[4]]
		send_mail(values)


def interactive_mode(values):
	print '-'*80
	print 'Interactive Mode'
	print '-'*80
	profile = select_profile(values[0])
	
	if profile[0] == 'default':
		p = raw_input('Profile (default): ')
		if p == '':
			profile[0] = 'default'
		else:
			profile[0] = p
		values[0] = select_profile(str(profile[0]))
	if args.html is False:
		h = raw_input('MIME (text or html): ')
		if h == 'html':
			values[4] = 'text/html'
		else:
			values[4] = 'text'
	if values[1] == 0:
		t = raw_input('To: ')
		values[1] = t
	if values[2] == 0:
		s = raw_input('Subject: ')
		values[2] = s
	if values[3] == 'empty':
		m = raw_input('Body File Path: ')
		values[3] = str(m)

	send_mail(values)


def batch_mode(values):
	# a. get file
	batch_file_path = str(args.batch)
	batch_file = open(os.path.expanduser(batch_file_path)) 
	mail_list = []
	# b. iterate file convert to list
	with batch_file as f:
		for line in f:
		    x = line.rstrip( )
		    mail_list.append(x)
		batch_file.close()
	# b. iterate list and send emails
	length = len(mail_list)
	cntr = 0
	while cntr < length:
		values[1] = mail_list[cntr]
		send_mail(values)
		print 'email sent to: '+str(mail_list[cntr])
		cntr += 1

def select_profile(profile):
	profile = str(profile)
	if profile == 'None':
		profile_name = 'default'
	else:
		profile_name = str(profile)
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

def send_mail(values):
	
    profile = values[0]
    to_email = values[1] #args.to
    from_email = profile[3]
    subject = values[2] #args.subject
    content_type = values[4]
    
    # parse message from text file
    header = "To:%s\nFrom:%s\nMIME-Version: 1.0\nContent-type: %s\nSubject:%s \n" % (to_email, from_email, content_type, subject)
	
	# extract message content from file
    file_name = values[3] #args.message
    the_file = open(file_name)
    msg = the_file.read()
    the_file.close()

    content = header + "\n" + msg
    smtpserver = initialize_smtp_server(profile)
    smtpserver.sendmail(from_email, to_email, content)
    smtpserver.close()
    
    #Print useful info
    print '='*80
    print 'e-mail sent'
    print '='*80
    print header
    print '-'*80
    print msg
    print '='*80
    
print '='*80
print 'gxmail - version %s' %(AppInfo['Version'])
print '='*80
test_profiles()
