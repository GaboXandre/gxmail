#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################
# GXMAIL - COMMAND LINE SMTP USER AGENT
###############################################################
#
#  gxmail.py
#  
#  Copyright 2014 GaboXandre <gabo.xandre@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import smtplib 
import sys
import os
import argparse 
import simplejson as json 

# GLOBAL VARIABLES
AppInfo = { 'AppName' : 'gxmail',
			'Version' : '1.1.6',
			'Author' : 'GaboXandre',
			'License' : 'GPL3',
			'copyright' : '2014 GaboXandre'
			}

FileLocations = { 'ProfileDir' : os.path.expanduser('~/.gxmail/')}


# Command Line Arguments
parser = argparse.ArgumentParser(description='%s is a simple text smpt client to send email from the command line. Very useful for scripts. If called without parameters, it starts in interactive mode.' %(AppInfo['AppName']))
parser.add_argument('-p', '--profile', help='Select profile to be used.', required=False)
parser.add_argument('-to', help='Receipient. You may include several email addresses separating them with a comma. DO NOT use spaces', required=False)
parser.add_argument('-s', '--subject', help='subject line.', required=False)
parser.add_argument('-m', '--message', help='Import email body from text file.', required=False)
parser.add_argument('-b', '--batch', help='Batch mode: get recepients from a text file.', required=False)
parser.add_argument('-html', '--html', help='HTML mode: send html formated content.', required=False, action="store_true")
parser.add_argument('-v', '--version', help='Prints version and exits program.', required=False, action="store_true")
parser.add_argument('-a', '--attachment', help='Send file attachment.', required=False)
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
	values = [args.profile, args.to, args.subject, args.message, 'text/plain', args.attachment]
	p = select_profile(values[0])
	t = str(args.to)
	s = str(args.subject)
	m = str(args.message)
	b = str(args.batch)
	h = args.html
	v = args.version
 	a = str(args.attachment)	

	int_mode = 'off'
		
	if h is True:
		values[4] = 'text/html'
	else:
		values[4] = 'text/plain'
	if a != 'None':
		a = os.path.expanduser(a) 
		values[5] = a
	else:
		values[5] = 'empty'	
	if t == 'None':
		values[1] = 0
		int_mode = 'on'
	if s == 'None':
		values[2] = 0
		int_mode = 'on'
	if m == 'None':
		values[3] = 'empty'
		int_mode = 'on'
	else:
		values[3] = os.path.expanduser(values[3])

	if b != 'None':
		values = [p, args.to, args.subject, args.message, values[4], values[5]]
		int_mode = 'off'
		batch_mode(values)
		
	if int_mode == 'on':
		interactive_mode(values)
	else:
		values = [p, args.to, args.subject, args.message, values[4], values[5]]
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
			values[4] = 'text/plain'
	if values[1] == 0:
		t = raw_input('To: ')
		values[1] = t
	if values[2] == 0:
		s = raw_input('Subject: ')
		values[2] = s
	if values[3] == 'empty':
		m = raw_input('Body File Path: ')
		m = os.path.expanduser(m) 
		values[3] = str(m)
	if values[5] == 'empty':
		question = raw_input('Include attachment?(y/n)-> ')
		if question == 'y':
			a = raw_input('Attachment: ')
			a = os.path.expanduser(a)
			values[5] = str(a) 
		else:
			values[5] = 'empty'

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
    xmailer = AppInfo['AppName']+'-v'+AppInfo['Version']
    marker = '2325769521'
    marker2 = '2325478522'
    marker3 = '2325478523'
    

	# extract message content from file
    file_name = values[3] #args.message
    the_file = open(file_name)
    msg = the_file.read()
    the_file.close()
    
    if values[5] == 'empty':
    	 # parse message from text file
    	header = "To:%s\nFrom:%s\nMIME-Version: 1.0\nContent-type: %s\nX-Mailer: %s\nSubject:%s \n" % (to_email, from_email, content_type, xmailer, subject)
    	
    	content = header + "\n" + msg
    	
    else:
		# attachment
		attachment_name = values[5]
		extract = open(attachment_name, 'r')
		encoded_attachment = extract.read()
		
		
		#Main Header
		header = """
		To:%s\n
		From:%s\n
		MIME-Version: 1.0\n
		X-Mailer: %s\n
		Subject:%s \n
		Content-Type: multipart/mixed; boundary=%s\n
		--%s\n
		Content-type: %s\n
		Content-Transfer-Encoding:8bit\n""" % (to_email, from_email, xmailer, subject, marker, marker, content_type)

		after_body = '--%s' %(marker)
		
		# attachment header
		attachment_header = '''
		Content-Type: text/plain; 
		name=\"%s\"\n
		Content-Disposition: attachment; filename=%s\n\n
		%s\n
		--%s--''' %(attachment_name, attachment_name, encoded_attachment, marker)

		content = header + "\n" + msg +"\n"+after_body+'\n'+attachment_header
    
    
    smtpserver = initialize_smtp_server(profile)
    smtpserver.sendmail(from_email, to_email, content)
    smtpserver.close()
    
    #Print useful info
    print '='*80
    print 'e-mail sent'
    print '='*80
    '''
    print header
    print '-'*80
    print msg
    print '='*80
    '''
    print content


if args.version is True:
	version_info = AppInfo['AppName']+'-v'+AppInfo['Version']
	print version_info
	quit()
	    
print '='*80
print 'gxmail - version %s' %(AppInfo['Version'])
print '='*80
test_profiles()
