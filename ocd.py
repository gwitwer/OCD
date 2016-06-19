import re

def remove_commas(l):
	line = l
	with_commas = [(m.start(0), m.end(0)) for m in re.finditer('\" *.+\, *.+\"', line)]
	#print(len(line), end=" - ")
	#print(len(with_commas), end=" = ")
	for section in with_commas:
		s = line[:section[0]]
		e = line[section[1]:]
		line = s + line[section[0]:section[1]].replace(',', '').replace('"', '') + e
	#print(len(line))
	return line

def test_col_length(year_data):
	if len(year_data) > 0:
		l = len(year_data[0])
		for d in year_data:
			if len(d) != l:
				break
		return (True, 'Columns have correct lengths.')
	return (False, "No Data!")

def remove_diocese_blanks(years_data):
	for y in years_data:
		while years_data[y]['Diocese'][-1] == '':
			years_data[y]['Diocese'].pop()

years = [
	# The data from 1966 - 1986 have inconsistent and problematic headings
    # '1966',
    # '1971',
    # '1976',
    # '1981',
    # '1986',
    '1991',
    '1996'
]

test_results = {}
years_data = {}

end = 2015
start = 1998
for x in range ((end + 1) - start):
    years.append(str(x + start))

for year in years:
	years_data[year] = {}
	year_data = []
	f = open('OCD1966-2015 - data_OCD' + year + '.csv', 'r')
	for line in f:
		# Remove commas from CSV line and split it (each line is a row)
		split_line = remove_commas(line).split(',')
			
		for col in range(len(split_line)):
			# initialize columns (will occur once)
			if (len(year_data) - 1) < col:
				years_data[year][split_line[col].rstrip('\n')] = []
				year_data.append([split_line[col].rstrip('\n')])
			# append data to correct col
			else:
				year_data[col].append(split_line[col])

	# print(year_data)
	for col in year_data:
		years_data[year][col[0]] = col[1:]
	#test(tests, test_results[year]) <-- If we have > 1 test, need to pass in correct data.
	#test_results[year] = [] 
	#test_results[year].append(test_col_length(year_data))

	f.close()
	# break;

remove_diocese_blanks(years_data)

target_vals = [
	'TotSemnr',
	'InfBapt',
	'MinorBapt',
	'AdltBapt',
	'RcvdFullComm',
	'FirstComm',
	'Conf',
	'TotMar',
	'TotCath'
]
# by_diocese = {}
# all_diocese = set([])
# for val in target_vals:
# 	by_diocese[val] = {}
# 	for y in years_data:
# 		by_diocese[val][y] = {}
# 		if val in years_data[y]:
# 			for i in range(len(years_data[y]['Diocese'])):
# 				all_diocese.add(years_data[y]['Diocese'][i])
# 				by_diocese[val][y][years_data[y]['Diocese'][i]] = years_data[y][val][i]
# 		else:
# 			print('FAIL: ' + y + ", " + val)

# for val in by_diocese:
# 	csv = []
# 	title_row = ['']
# 	for d in sorted(all_diocese):
# 		title_row.append(d)
# 	csv.append(','.join(title_row))
# 	for y in sorted(by_diocese[val]):
# 		csv_row = []
# 		for d in sorted(all_diocese):
# 			if d in by_diocese[val][y]:
# 				csv_row.append(by_diocese[val][y][d])
# 			else:
# 				csv_row.append('')
# 		csv_row.insert(0, y)
# 		csv.append(','.join(csv_row))
# 	f = open(val+'.csv', 'w')
# 	f.write('\n'.join(csv))
# 	f.close()

by_diocese = {}
all_diocese = set([])
for val in target_vals:
	by_diocese[val] = {}
	for y in years_data:
		by_diocese[val][y] = {}
		if val in years_data[y]:
			# This gets messy because of many inconsistencies!
			for i in range(len(years_data[y]['Diocese'])):
				# remove archdiocese
				# years_data[y]['Diocese'][i] = name of diocese
				if years_data[y]['Diocese'][i].find('(Archdiocese)') < 0:
					# Fix misspellings of Ukrainian
					if years_data[y]['Diocese'][i].find('Ukra') < 0:
						# Fix misspelling of Bismarck
						if years_data[y]['Diocese'][i].find('Bismark') < 0:
							# Fix inconsistent location markup
							fixes = {
								'KS': 'in Kansas',
								'IL': 'in Illinois',
								'IN': 'in Indiana',
								'': 'in California',
								'OR': 'in Oregon',
								'MA': 'in Massachusetts',
								'TX': 'in Texas',
								'of Lebanon of L.A.': 'of Lebanon of Los Angeles',
								'Great Falls-Billings': 'GreatFalls-Billings',
								'Worcester': 'Worchester',
								'Victoria': 'Victoria TX',
								'Reno': 'Reno-Las Vegas',
								'St. Maron': 'St. Maron Brooklyn'
							}
							fixed_diocese = years_data[y]['Diocese'][i]
							for k in fixes:
								fixed_diocese = re.sub(fixes[k], k, fixed_diocese)
							fixed_diocese = fixed_diocese.rstrip()

							# special fix
							if fixed_diocese == 'Lafayette':
								fixed_diocese = 'Lafayette LA'
							all_diocese.add(fixed_diocese)
							by_diocese[val][y][fixed_diocese] = years_data[y][val][i]

						else:
							by_diocese[val][y]['Bismarck'] = years_data[y][val][i]
					else:
						fixed_diocese = years_data[y]['Diocese'][i]
						fixed_diocese = re.sub(' - ', ' ', fixed_diocese)
						fixed_diocese = re.sub('Chicago', '', fixed_diocese)
						fixed_diocese = re.sub('-', ' ', fixed_diocese)
						fixed_diocese = fixed_diocese.split(' ')
						fixed_diocese = ' '.join(fixed_diocese[:-1]).rstrip() + ' - Ukrainian'
						all_diocese.add(fixed_diocese)
						by_diocese[val][y][fixed_diocese] = years_data[y][val][i]
				else:
					# by_diocese[val][y][years_data[y]['Diocese'][i]] = years_data[y][val][i]
					# print(by_diocese[val][y][years_data[y]['Diocese'][i]])
					# print(by_diocese[val])
					fixed_diocese = years_data[y]['Diocese'][i].split(' ')
					fixed_diocese = ' '.join(fixed_diocese[:-1])
					by_diocese[val][y][fixed_diocese] = years_data[y][val][i]
		else:
			print('FAIL: ' + y + ", " + val)
for val in by_diocese:
	csv = []
	title_row = ['']
	for y in sorted(by_diocese[val]):
		title_row.append(y)
	# csv.append(','.join(title_row))
	for d in sorted(all_diocese):
		csv.append([d])
	for y in sorted(by_diocese[val]):
		for row in csv:
			if row[0] in by_diocese[val][y]:
				row.append(by_diocese[val][y][row[0]])
			else:
				row.append('')
		# csv_row.insert(0, y)
		# csv.append(','.join(csv_row))
	for r in range(len(csv)):
		csv[r] = ','.join(csv[r])
	csv.insert(0, ','.join(title_row))
	f = open(val+'.csv', 'w')
	f.write('\n'.join(csv))
	f.close()



fail = False
for y in test_results:
	for r in test_results[y]:
		if r[0]:
			print("SUCCESS: " + r[1])
		else:
			print("FAIL: " + r[1])
			fail = True
if fail:
	print("TESTS FAILED")
else:
	print("ALL TESTS PASS!")
