#!/usr/bin/env python3

'''####################################
#Reasons for imports
	mako.template	: used for using the mako template language for the latex resume
	json			: used for reading the Info.json files
	yaml			: used for writing the website data files
	os				: used for verifying and reading files
	sys				: used for file paths
	calendar		: used for the month/number conversion
	re				: used for regular expressions
'''####################################

from mako.template import Template
import json
import yaml
import os
import sys
import calendar
import re

'''####################################
#The main class that does the latex and handles the website conversions
'''####################################
class hold:
	def __init__(self,foils):
		self.info = json.load(open(foils[0],'r'))
		self.fileName = foils[0]
		self.latex = True if len(foils) == 3 else False
		if len(foils) == 2:
			self.outputDir = foils[1]
		else:
			self.template = foils[1]
			self.newFile  = foils[2]
	def __str__(self):
		return json.dumps(self.info, default=lambda o: o.__dict__, sort_keys=True, indent=3)
	def __print__(self):
		print(str(self))
	'''####################################
	#The main method within the class that handles the conversions
	'''####################################
	def render(self):
		if (self.latex):
			newInfo = (Template(filename=self.template).render(**self.info))
			newInfo = newInfo.replace('\\\\\\','\\\\').replace('\\\\','\\\\\n').replace('#','\#').replace('<','$<$').replace('>','$>$')
			with open(self.newFile,'w') as file:
				##Removing Comments
				for line in newInfo.split('\n'):
					if (not line.strip().startswith('%')):
						file.write(str(line)+'\n')
		else:
			for key, value in self.info.items():
				if key not in ['me','newTech', 'interests']:
					with open(os.path.join(self.outputDir, str(key)+'.yml'), 'w') as skillFile:
						skillFile.write(website.convertList(key, value))
				elif key in ['interests']:
					with open(os.path.join(self.outputDir, str(key)+'.yml'), 'w') as skillFile:
						skillFile.write(yaml.dump(website.convertItem(key, value),default_flow_style=False))

'''####################################
#A utility class that contains the filters for the website yaml files
'''####################################
class website:
	def extLines(skill):
		lyst = skill['lines']
		if 'extraLines' in skill:
			lyst += skill['extraLines']
		return lyst

	def niceDates(fromDate, toDate):
		string = str(website.nameMonth(fromDate))

		if (fromDate != toDate):
			string += ' - ' + str(website.nameMonth(toDate))

		return string

	def filter(string):
		string = str(string)
		if not string or string == None or string == "None" or not string.strip():
			return ''
		else:
			return string.strip()

	def nameMonth(date):
		month = re.match(r'([0-9]{2})\/',date)
		if month:
			return str(calendar.month_name[int(month.group(1))]) + " " + str(date[3:])
		else:
			return date

	def itemizeList(descList):
		string = ""
		for desc in descList:
			string += "*  " + desc.strip() + ".\n"
		return string

	def concatList(descList):
		string = ""
		for desc in descList:
			if desc == '':
				string += "\n"
			else:
				string += desc.strip() + ".\n"
		return string

	def convertItem(key, value):
		return {
			"skills": website._skill,
			"education": website._edu,
			"experience": website._exp,
			"groups": website._grp,
			"projects": website._proj,
			"interests": website._interest
		}[key](value)

	def convertList(key, value):
		return yaml.dump([website.convertItem(key,skill) for skill in value], default_flow_style=False)

	def _interest(skill):
		return {
			"more_content": str(website.itemizeList(skill)).replace(".","")
		}

	def _proj(skill):
		return {
			"name": skill['name'],
			"github": None if 'github' not in skill else skill['github'],
			"dates": website.niceDates(skill['from'], skill['to']),
			"description": skill['description']
		}

	def _grp(skill):
		return {
			"name": skill['Name'],
			"link": skill['URL'],
			"quote": skill['Quote'],
			"qualification": skill['Position'],
			"dates": website.niceDates(skill['Start'], skill['End']),
			"description": website.concatList(skill['lines'])
		}

	def _exp(skill):
		return {
			"company": skill['name'],
			"link": skill['URL'],
			"job_title": skill['title'],
			"qualification": skill['qualification'],
			"dates": website.niceDates(skill['Start'], skill['End']),
			"description": website.itemizeList(website.extLines(skill)),
			"learned": skill['Learnt']
		}

	def _skill(skill):
		return {
			"name": skill['name'],
			"link": skill['link'],
			"percentage": skill['percent'],
			"projects": website.filter(skill['numProj']),
			"dates": website.niceDates(skill['from'], skill['to'])
		}

	def _edu(edu):
		return {
			"name": edu['Name'],
			"link": edu['URL'],
			"dates": website.niceDates(edu['Start'], edu['Grad']),
			"qualification": str(edu['Qualification']) + ' ' + str(edu['Major']),
			"quote": edu['Quote'],
			"description": website.concatList(edu['Description'])
		}

'''####################################
#The method that checks for file validity
'''####################################
def fileCheck(file, ext, updateFile=True):
		split=file.split('.')

		if (ext is not None):
			if (len(split) != 2):
				print(str(file)+' is not a valid file.')
				sys.exit()

			if (split[1] != ext):
				print(str(file) + ' is a valid '+str(ext)+' file.')
				sys.exit()
			
			if ( (updateFile and not os.path.isfile(file)) or (not updateFile and os.path.isfile(file))):
				print('Please fix file '+str(file))
				sys.exit()
		else:
			if (not os.path.isdir(file)):
				print('Directory ' + str(file) + ' does not exist')
				sys.exit()

if __name__ == "__main__":
	if (len(sys.argv) != 4 and len(sys.argv) != 3):
		print('Usage 1: ./make.py x y z')
		print('\tx :=')
		print('\tJson File ~ create the pdf')
		print('\tTemplate Latex File')
		print('\tNew File Name')
		print('Usage 2: ./make.py x y')
		print('\tx :=')
		print('\tJson File ~ create the pdf')
		print('\tWebsite output directory')
		sys.exit()

	if len(sys.argv) == 4: #Latex
		files,check=[sys.argv[1],sys.argv[2],sys.argv[3]],['json','tex','tex']
	else: #Website
		files,check=[sys.argv[1],sys.argv[2]],['json',None]

	for num, file in enumerate(files):
		fileCheck(file, check[num], False if num == 2 else True)

	info = hold(files)
	info.render()