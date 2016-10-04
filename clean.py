import csv
import re
import phonenumbers

# Simple Regex for syntax checking
email_regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

name_regex = '^[a-zA-Z .\'-]+$'

def check_email(value):
		
	#if email is empty return
	if len(value) < 6:
		return ''
		
	#strip all spaces
	value = value.strip(' ');
	
	# Syntax check
	match = re.match(email_regex, value)
	if match == None:
		print('Bad Email Syntax')
		return ''

	# Get domain for DNS lookup
	splitAddress = value.split('@')
	domain = str(splitAddress[1])
	print('Domain:', domain)

	#TODO: check domain against a list of valid domains and use soundex to correct misspelled domains or try dnslookup on their MX record
	
	return value

def check_phone(value):
		
	#if phone is empty return
	if len(value) < 10 :
		return value
		
	
	#strip all spaces
	value = value.strip(' ');
	value = value.strip('(');
	value = value.strip(')');
	value = value.strip('-');
	
	if value[0]!='+':
		value = '+' + value
	
	try:
		phone = phonenumbers.parse(value, None)
		print('Phone:',phone)
	except phonenumbers.phonenumberutil.NumberParseException:
		return '';
		
	if not phonenumbers.is_valid_number(phone):
		return ''
		
	if not phonenumbers.is_possible_number(phone):
		return ''
	
	return value

def check_name(value):
		
	#if name is empty return
	if len(value) < 3 or len(value) > 60 :
		return ''
		
	#if too many names, take first and last
	names = value.split(' ')
	
	if len(names) > 2:
		value = value[0] + " " + value[len(names)-1]
		
	# Syntax check
	match = re.match(name_regex, value)
	if match == None:
		print('Bad Name Syntax')
		return ''
	
	return value
	
def clean_up_data():
	# open the csv file
	print("Opening file...")
	
	clean_data = []
	
	with open('data.csv', encoding="utf-8") as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			print(row['name'], row['phone'], row['email'])
			row['name'] = check_name(row['name'])
			row['phone'] = check_phone(row['phone'])
			row['email'] = check_email(row['email'])
			
			if len(row['name'])==0 or len(row['phone'])==0 or len(row['email'])==0:
				continue
			
			if len(row['email'])==0 and len(row['phone'])==0:
				continue
				
			print(row['name'], row['phone'], row['email'])
			clean_data.append(row)


	with open('cleandata.csv', 'w') as csvfile:
		fieldnames = ['name', 'phone', 'email']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for row in clean_data:
			writer.writerow(row)
    
	

# entry point for app
if __name__ == "__main__":
	print("Beginning Script...")
clean_up_data()