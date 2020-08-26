import re
import operator
import csv
import sys


def get_user_for_log_file(log_file):
	list_of_user = []
	with open(log_file,'r') as file:
		for line in file.readlines():
			user_name = re.findall(r'\([\w\.]*\)',line.strip())
			list_of_user.append(''.join(user_name))

		remove_duplicat = set(list_of_user)
		data = {}
		for user in remove_duplicat:
			data[user] = [user.strip('()'),0,0]
	return data

def change_value_in_data(data):
	with open(log_file,'r') as file:
		for line in file.readlines():
			for user in data:
				if user in line.strip():
					if 'ERROR' in line.strip():
						data[user][1] += 1
					elif 'INFO' in line.strip():
						data[user][2] += 1
	cleaned_data = {}
	for key in data.keys():
		cleaned_data[data[key][0]] = [data[key][2],data[key][1]]
	chaatna = sorted(cleaned_data.items(), key=operator.itemgetter(0))
	return chaatna

def dict_to_csv(dictionary):
	with open('user_statistics.csv', 'w', newline='') as output_csv:
		writer = csv.DictWriter(output_csv, fieldnames=['Username', 'INFO','ERROR'])
		writer.writeheader()
		for num in range(len(dictionary)):
			writer.writerow({'Username': dictionary[num][0], 'INFO': dictionary[num][1][0],'ERROR': dictionary[num][1][1]})



log_file = sys.argv[1]
data = get_user_for_log_file(log_file)
master = change_value_in_data(data)
dict_to_csv(master)
print('Your CVS HAS Created')
print('\n')

list_of_error = []
list_of_info = []

error_list = ['Timeout while retrieving information',
				'The ticket was modified while updating',
				'Connection to DB failed',
				'Tried to add information to closed ticket',
				'Permission denied while closing ticket',
				'Ticket doesn\'t exist']

with open(log_file, 'r') as file:
	count_of_errors = 0
	coun_of_info = 0
	for line in file.readlines():
		if re.search(r"ticky: ERROR ([\w ]*) ",line.strip()):
			list_of_error.append(line.strip())
			count_of_errors += 1
		elif re.search(r'ticky: INFO ([\w ]*) (\[#\d{4}\]) ',line):
			list_of_info.append(line.strip())
			coun_of_info += 1

#this code create CSV for error
dict_with_error_count = {}
for error in error_list:
	counter = 0
	for present in range(len(list_of_error)):
		if error in list_of_error[present]:
			counter += 1
	dict_with_error_count[error] = counter

sorted(dict_with_error_count, key=operator.itemgetter(1), reverse=True)

with open('error_message.csv', 'w', newline='') as output_csv:
	writer = csv.DictWriter(output_csv, fieldnames=['Error', 'Count'])
	writer.writeheader()
	for k,v in dict_with_error_count.items():
		writer.writerow({'Error':k, 'Count':v})





