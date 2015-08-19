import os.path
import sys
from csv import DictReader


'''
budget_validator_parser.py - a tool for importing budgets' sheets and outputing them in a standardized manner

A Valid form for a municipal budget item includes:

(1 - denotes regular budget) (.) (1-4 digit mandatory code) (2 digit discretionary code) (.) (1-3 digit code type or 000 if no type).
For example: 

1.3132 01.420 
or 
1.0121 00.290

More info can be found here: 
http://www.moin.gov.il/Subjects/TaktzivRagil/Pages/VaadatHacsafim.aspx
And more specifically, here:
http://www.moin.gov.il/SubjectDocuments/Perek3.pdf (page 7+)
http://www.moin.gov.il/SubjectDocuments/Nispach4.pdf

Pseudo code for what we do here:

1) Get a budget item (code in an unknown form), and analyze it:

	1a) Containing dots? if 2 dots exist (as required):
		Check 1. is the prefix, fail (utterly!) if it isn't => this is an irregular (="pituach") budget.

	1b) Only 1 dot? Assume everything before dot is code, and after dot is type. 

	1c) No dots? Handle based on the following:


2) Check if the string contains 10 digits (the most common case, AFAIK). 
Assume 1st digit is "1", else fail. (not a "regular" budget!).

If it is - split to 6 digits of code + 3 digits of type
If 6 digits only, assume it's item (without code) only. "Split" to 6 + type "000".

3) Next, delete all zeroes from the end, to see what we're left with. 

4) If remaining code length is 4 to 6 digits, assume the first 4 digits are legal code, and "inflate" the budget item 
with a leading zero for the last two digits if needed, until we have 4 original code digits, and 2 discretionary 
(for example, for code 6111, output 611100, and for 61111 output 611101!).

5) For 4 digits or less, simply insert leading zeros until we have 4 digits (61 -> 0061), 2 discretionary zeroes.  

Voilla!

'''


class Budget_Validator(object):

	'''	Set the configuration needed for the validator for a certain budget

		:param file_name - relative path to the budget filename
		:param field_names - a list of integer idices descibing the fields, always on the order:
		["budget code","budget code type", "budget amount", "actual amount"], where the only MANDATORY fields
		are the "budget code" and either "budget / actual" amounts (since some of the amounts and the type 
		may be empty for a budget line item).
		:param out_file_name - relative path to the CSV filename to be written with the correct budget items
		:param out_erroneous_filename - relative path to the CSV filename to be written with the erroneous budget items

	'''
	def __init__(self,file_name,field_names,out_file_name,out_erroneous_filename):

		if (not file_name or os.path.isfile(file_name)):
			raise ValueError("Bad / nonexistent file name.")

		self.file_name = file_name

		if (not out_file_name):
			raise ValueError("Bad / nonexistant out file name.")

		self.out_file_name = out_file_name		

		if (not type(field_names) == types.ListType or (not len(field_names) == 4)):
			raise ValueError("field names - should be exactly four integers, representing code, type, budget, actual indices, \
							 or -1 if these don't exist")

		elif (field_names[2] == -1 and field_names[2]== -1):
			raise ValueError("file should contain at least budget or actual amounts.")

		self.field_names=field_names

		if (not out_erroneous_filename):
			raise ValueError("Bad erroneous file name.")

		self.out_erroneous_filename = out_erroneous_filename


	def validate(self):


		with open(file_name) as infile, open (out_file_name, "wb") as outfile:
		    reader = csv.reader(infile)
		    writer = csv.writer(outfile, delimiter=",")
		    for d in reader:
		        print d




if __name__ == "__main__":
	print("Budget Item Validator tool: converts general budget item into a standardized format")
	print("USAGE: python budget_item_validator.py {path to filename} {list containing fields} {outfile} {logfile}")
	print("params: {} {} {}").format(sys.argv[1],sys.argv[2],sys.argv[3])
