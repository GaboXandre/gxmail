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

def initialize_smtp_server(arguments):
	server = arguments[0][1]
	port = arguments[0][2]
	email = arguments[0][3]
	password = arguments[0][4]
	smtpserver = smtplib.SMTP(server, port)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	smtpserver.login(email, password)
	return smtpserver

def send_mail(arguments):
	print 'Sending email ... '
	######################################################	
	# 1. Common Variables
	######################################################
	to_email = arguments[1]
	from_email = arguments[0][3]
	subject = arguments[2]
	mime_type = arguments[4]
	xmailer = AppInfo['AppName']+'-v'+AppInfo['Version']
	attachment = str(arguments[5])
	
	######################################################	
	# 2. Extract message from file
	######################################################
	file_name = arguments[3] #args.message
	the_file = open(file_name)
	msg = the_file.read()
	the_file.close()
	######################################################
	# 3a. Prepare email without attachment
	######################################################
	if attachment == 'None':

		# parse message from text file
		header = "To:%s\nFrom:%s\nSubject:%s\nX-Mailer: %s\nContent-type: %s\n " % (to_email, from_email, subject, xmailer, mime_type)
		content = header + "\n" + msg
		
	######################################################
	# 3b. Prepare email with attachment
	######################################################	
	else:
		marker = '2325769521'
		
		# prepare attachment
		attachment_name = arguments[5]
		extract = open(attachment_name, 'r')
		encoded_attachment = extract.read()
		
		#Main Header
		header = "To:%s\nFrom:%s\nMIME-Version: 1.0\nX-Mailer: %s\nSubject:%s\nContent-Type: multipart/mixed; boundary=%s\n--%s\nContent-type: %s\nContent-Transfer-Encoding:8bit\n" % (to_email, from_email, xmailer, subject, marker, marker, mime_type)

		after_body = '--%s' %(marker)
		
		# attachment header
		attachment_header = "Content-Type: text/plain; name=\"%s\"\nContent-Disposition: attachment; filename=%s\n%s\n--%s--" %(attachment_name, attachment_name, encoded_attachment, marker)

		content = header + "\n" + msg +"\n"+after_body+'\n'+attachment_header
		
	######################################################
	# 4. Send email 
	######################################################
	
	try:
		smtpserver = initialize_smtp_server(arguments)
		smtpserver.sendmail(from_email, to_email, content)
		smtpserver.close()
		print 'e-mail sent successfully to '+str(to_email)
		print '='*80
	except Exception:
		print 'Opps, the email could not be sent.'
		print '='*80
	

	
	
	
def batch_mode(arguments):
	print 'you are now in batch mode...' ##########DEBUG
	############################################
	# 0. Prepare arguments
	############################################
	mime_type = arguments[4]
	if mime_type is True:
		arguments[4] = 'text/html'
	else:
		arguments[4] = 'text/plain'
	
	
	############################################
	# 1. Get the file with emails
	############################################
	batch_file_path = str(arguments[7])
	batch_file = open(os.path.expanduser(batch_file_path)) 
	
	############################################
	# 2. Itirate file to make the list
	############################################
	mail_list = []
	with batch_file as f:
		for line in f:
		    x = line.rstrip( )
		    mail_list.append(x)
		batch_file.close()
	
	############################################
	# 3. Iterate list and send emails
	############################################
	length = len(mail_list)
	cntr = 0
	while cntr < length:
		arguments[1] = mail_list[cntr]
		send_mail(arguments)
		#print 'email sent to: '+str(mail_list[cntr])
		#print '-'*80
		cntr += 1
	############################################
	# DEBUG INFO
	############################################
	print batch_file_path
	print mail_list

def interactive_mode():
	print '-'*80
	print 'Interactive Mode'
	print '-'*80
	############################################
	# 0. Start the list with no values
	############################################
	global arguments
	arguments = []
	print arguments

	############################################
	# 1. Get main input
	############################################
	p = raw_input('Profile (default): ')
	if p == '':
		arguments.append('None')
	else:	
		arguments.append(str(p))
	h = raw_input('MIME (text or html): ')
	if h == 'html':
		h = 'text/html'
	else:
		h = 'text/plain'
	t = raw_input('To: ')
	s = raw_input('Subject: ')
	m = raw_input('Body File Path: ')
		 
	
	############################################
	# 2. Start the list
	# [0-profile, 1-to, 2-subject, 3-message, 4-text/html, 5-attachment, 6-interactive, 7-batch, 8-version ]
	############################################

	arguments.append(str(t))
	arguments.append(str(s))
	arguments.append(os.path.expanduser(m))
	arguments.append(h)
	
	
	############################################
	# 3. Attachment?
	############################################
	question = raw_input('Include attachment?(y/n)-> ')
	if question == 'y':
		a = raw_input('Attachment: ')
		a = os.path.expanduser(a)
		arguments.append(os.path.expanduser(a))
	else:
		a = 'None'
		arguments.append(str(a))
	
	############################################
	# 3. Get profile info
	# Note this seciton is copy paste from select_profile
	# Shame on me !!!!! 
	############################################
	
	profile = str(arguments[0])
	if profile == 'None':
		profile_name = 'default'
	else:
		profile_name = profile
	profile_location = FileLocations['ProfileDir']+profile_name
	# load profile info
	myfile = open(profile_location)
	myfile2 = myfile.read()
	profile = json.loads(myfile2)
	arguments[0] = profile
	
	############################################
	# 3. Send email
	############################################
	arguments.append(False)
	arguments.append('None')
	arguments.append(False)
	send_mail(arguments)


	


def test_options(arguments):
	######################################################	
	# Select Profile
	######################################################	
	profile = str(arguments[0])
	if profile == 'None':
		profile_name = 'default'
	else:
		profile_name = profile
	profile_location = FileLocations['ProfileDir']+profile_name
	# load profile info
	myfile = open(profile_location)
	myfile2 = myfile.read()
	profile = json.loads(myfile2)
	arguments[0] = profile
	
	############################################
	# 1. Check general options
	# 	a. version
	#	b. interactive
	#	c. batch
	############################################ 
	version = arguments[8]
	interactive = arguments[6]
	batch = str(arguments[7])
	
	if version is True:
		version_info = AppInfo['AppName']+'-v'+AppInfo['Version']
		print version_info
		quit()
	
	if batch != 'None':
		batch_mode(arguments)
		quit()
	
	if interactive is True:
		interactive_mode()
		quit()
	
	######################################################	
	# 2. Check email option and pass them to send_email()
	#	1. to
	#	2. subject
	#	3. message
	#	4. type: text or html
	#	5. attachment #### should t be here?
	######################################################	
	to = str(arguments[1])
	subject = str(arguments[2])
	message = str(arguments[3])
	mime_type = arguments[4]
	attachment = str(arguments[5])
	switch = 'ON'
	# test that all mandatory arguments are included
	if to == 'None':
		switch = 'OFF'
	if subject == 'None':
		switch = 'OFF'
	if message == 'None':
		switch = 'OFF'
	
	if switch == 'OFF':
		print 'Sorry, information is missing...\nUse flag -h or --help \nAlso, you may use interactive mode with flag -i or --interactive.'
		quit()

	#switch == 'ON', so we continue testing...

	if mime_type is True:
		arguments[4] = 'text/html'
	else:
		arguments[4] = 'text/plain'
	
	
	######################################################	
	# 3. READY TO SEND EMAIL
	######################################################	
	send_mail(arguments)
	

def create_profile(defprofile):
	try:
		default_file = FileLocations['ProfileDir']+'/default'
		default = open(default_file, 'w')
			
		default.write(json.dumps(defprofile))
		default.close()
		res = 'You are ready to send emails with your new profile!'
		print res
	except Exception:
		print 'Error: Default profile could not be created. Sorry.'
		quit()


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

def main():
	
	global AppInfo
	global FileLocations
	global arguments
	AppInfo = { 'AppName' : 'gxmail',
			'Version' : '1.1.7',
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
	parser.add_argument('-i', '--interactive', help='Runs in interactive mode.', required=False, action="store_true")
	parser.add_argument('-a', '--attachment', help='Send file attachment.', required=False)
	args = parser.parse_args()
	
	# list format:
	# [0-profile, 1-to, 2-subject, 3-message, 4-text/html, 5-attachment, 6-interactive, 7-batch, 8-version ]
	arguments = [args.profile, args.to, args.subject, args.message, args.html, args.attachment, args.interactive, args.batch, args.version]
	print '='*80
	print 'gxmail - version %s' %(AppInfo['Version'])
	print '='*80
	
	return arguments
	
		

if __name__ == '__main__':
	main()
	test_profiles()
	test_options(arguments)

