import sys
import os
import time
import datetime
import re
import markdown
import html

root_path       = "c:\\temp\\blog"               # Path to read markdown files from
blog_title      = "blog.jonbeckett.com"          # Title of Blog
author_name     = "Jonathan"                     # Name to give author of each post
blog_url        = "https://blog.jonbeckett.com"  # URL of blog
today_date      = "2019-12-17T00:00:00Z"         # Today's date
post_category   = "Life"                         # Default category for each post
output_filename = "c:\\temp\\md2blogger.xml"     # Output filename


# Start the XML
xml = ("<?xml version='1.0' encoding='UTF-8'?>\r\n"
    "<ns0:feed xmlns:ns0=\"http://www.w3.org/2005/Atom\" xmlns:ns1=\"http://purl.org/syndication/thread/1.0\">\r\n"
    "<ns0:title type=\"html\">" + blog_title + "</ns0:title>\r\n"
    "<ns0:generator>Blogger</ns0:generator>\r\n"
    "<ns0:link href=\"" + blog_url + "\" rel=\"self\" type=\"application/atom+xml\" />\r\n"
    "<ns0:link href=\"" + blog_url + "\" rel=\"alternate\" type=\"text/html\" />\r\n"
    "<ns0:updated>" + today_date + "</ns0:updated>\r\n")

i=0

for subdir, dirs, files in os.walk(root_path):
	for file in files:
		if '.md' in file and 'README.md' not in file:
            
			print("Processing " + file)
			
			i = i + 1
            
			# Read the file contents
			markdown_file_full_path = os.path.join(subdir, file)
			markdown_file = open(markdown_file_full_path,'r')
			markdown_text = markdown_file.read()
			
			# split the line into files, and chop the top 4 off
			# (to get rid of the title and date, as output by wp2md)
			markdown_text_lines = markdown_text.splitlines()
			hybrid_text_lines = []
			hybrid_text_lines += markdown_text_lines[4:]
			
			# build the post title and body
            
            # Title
			post_title              = markdown_text_lines[0].replace('# ','')
			post_title_html_escaped = html.escape(post_title)
            
            # Body
			post_body              = '\r\n'.join(hybrid_text_lines)
			post_body_html         = markdown.markdown(post_body)
			post_body_html_escaped = html.escape(post_body_html)
            
			# Extract the date from the filename
			# (so we may use it to back-date the post into write.as)
			year      = file[0:4]
			month     = file[5:7]
			day       = file[8:10]
			post_date = year + '-' + month + '-' + day + 'T00:00:00Z';
            
			xml = xml + '<ns0:entry>\n'
			xml = xml + '<ns0:category scheme=\"http://www.blogger.com/atom/ns#\" term=\"' + post_category + '\" />\n'
			xml = xml + '<ns0:category scheme="http://schemas.google.com/g/2005#kind" term="http://schemas.google.com/blogger/2008/kind#post" />\n'
			xml = xml + '<ns0:id>' + str(i) + '</ns0:id>\n'
			xml = xml + '<ns0:author><ns0:name>' + author_name + '</ns0:name></ns0:author>\n'
			xml = xml + '<ns0:content type=\"html\">' + post_body_html_escaped + '</ns0:content>\n'
			xml = xml + '<ns0:published>' + post_date + '</ns0:published>\n'
			xml = xml + '<ns0:title type=\"html\">' + post_title_html_escaped + '</ns0:title>\n'
			xml = xml + '</ns0:entry>\n'
        
    



# End the XML
xml = xml + "</ns0:feed>\r\n"

# Output the XML to a file
post_file = open(output_filename, "w")
post_file.write(xml)
post_file.close()

