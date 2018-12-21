import os
import datetime
from random import randint

def process_txt(filename):
	"""Take one cnmarc text file at a time, and write the output into an text file.
	f is the file name(string). 
	"""
	fout = open('output.txt', 'w')
	fin = open(filename)
	now = datetime.datetime.now()
	for line in fin:
		if line[:3] == 'FMT':
			leader = '=LDR  00000nam a2200000Ia 45e0\n'
			fout.write(leader)
			control_number = randint(1000000000, 9999999999)
			control_number_temp = 'hd%d' % control_number
			tag001 = '=001  ' + control_number_temp + '\n'
			fout.write(tag001)
			tag003 = '=003  HU-BpHD\n'
			fout.write(tag003)
			tag005 = '=005  ' + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + '.0\n'
			fout.write(tag005)
			tag040 = '=040  \\\\$aFrPJT$cFrPJT\n'
			fout.write(tag040)


		elif line.strip()[:3] == '010':
			newline = line.split('|')
			for word in newline:
				#Get Chinese Title
				if word[0] == 'a':
					isbn= word[1:]
					new_isbn = '$a' + isbn.replace('-', '').strip()
				elif word[0] == 'd':
					price = '$c' + word[1:].strip()
			tag020 = '=020  \\\\' + new_isbn + price + '\n'
			fout.write(tag020)

		elif line.strip()[:3] == '101':
			newline = line.split('|')
			language =[]
			for word in newline:
				#Get original language
				if word[0] == 'a':
					original_lang = '$a' + word[1:].strip()
					language.append(original_lang)
				elif word[0] == 'c':
					tranlation_lang = '$h' + word[1:].strip()
					language.append(tranlation_lang)
			tag041 = '=041  1' + '\\' + ''.join(language) +'\n'
			fout.write(tag041)

		elif line.strip()[:3] == '200':
			newline = line.split('|')
			title =[]
			full_author = []
			for word in newline:
				#Get Chinese Title
				if word[0] == 'a':
					cntitle = '$a' + word[1:].strip() +'.'
					title.append(cntitle)

				#Get serial number title
				elif word[0] == 'h':
					serial_title =word[1:].strip()
					title.append(serial_title)

				elif word[0] == 'i':
					sub_title = ',' +word[1:].strip() + '.'
					title.append(sub_title)

				#Get Pinyin Title
				elif word[0] == '9':
					pinyinTitle='$b' + word[1:].strip()
					title.append(pinyinTitle)
				elif word[0] == 'f':
					author1 = word[1:].strip()
					full_author.append(author1)
				elif word[0] == 'g':
					author2 =';' + word[1:].strip()
					full_author.append(author2)

				#Get the main author
#				elif word[0] == 'f':
#					author_main = word[1:].strip()
#			tag100 = '=100  1\\$a' + author_main + '\n'
#			fout.write(tag100)
			tag245 = '=245  10' + ''.join(title) + '$c' + ''.join(full_author) + '\n'
			fout.write(tag245)
		elif line.strip()[:3] == '210':
			newline = line.split('|')
			for word in newline:
				#Location
				if word[0] == 'a':
					location=word[1:].strip()
				#Publisher
				elif word[0] == 'c':
					publisher=word[1:].strip()

				#Year
				elif word[0] == 'd':
					date_pub=word[1:].strip()
			tag260 = '=260  \\\\$a' + location + '$b' + publisher + '$c' + date_pub + '\n'
			fout.write(tag260)
			tag00800 = str(now.year)[2:] + str(now.month) + str(now.day)
			tag00806 = 's'
			tag00807 = date_pub
			tag00811 = '\\\\\\\\'
			tag00815 = 'ch\\'
			tag00818 ='||||||||||||||\||'
			tag00835 = 'chi'
			tag008 = '=008  ' + tag00800 + tag00806 + tag00807 + tag00811 + tag00815 + tag00818 + tag00835 + '\n'
			fout.write(tag008)
	
		elif line.strip()[:3] == '215':
			newline = line.split('|')
			hold300 =[]
			for word in newline:
				#Pages
				if word[0] == 'a':
					extent='$a' + word[1:].strip()
					hold300.append(extent)

				#Discription
				elif word[0] == 'c':
					discription='$c' + word[1:].strip()
					hold300.append(discription)

				#Dimension	
				elif word[0] == 'd':
					dimention = '$d' + word[1:].strip()
					hold300.append(dimention)

			tag300 = '=300  \\\\' + ''.join(hold300) + '\n'
			fout.write(tag300)
			print 'tag300 okay'

		elif line.strip()[:3] == '225':
			newline = line.split('|')
			hold440 = []
			for word in newline:
				#series_title
				if word[0] == 'a':
					series_title = '$a' + word[1:].strip()
					hold440.append(series_title)
				#subseries number
				elif word[0] == 'h':
					subseries_number = '$n' + word[1:].strip()
					hold440.append(subseries_number)
				#subseries_title
				elif word[0] == 'i':
					subseries_title = '$p' +word[1:].strip()
					hold440.append(subseries_title)
				#volume
				elif word[0] == 'v':
					volume = '$v' + word[1:].strip()
					hold440.append(volume)

			tag440 = '=440  \\\\' + ''.join(hold440) + '\n'
			fout.write(tag440)

		elif line.strip()[:3] == '300':
			newline = line.split('|')
			for word in newline:
				#general note
				if word[0] == 'a':
					general_note = word[1:].strip()
			tag500 = '=500  \\\\$a' + general_note + '\n'
			fout.write(tag500)

		elif line.strip()[:3] == '330':
			newline = line.split('|')
			for word in newline:
				#summary note
				if word[0] == 'a':
					summary = word[1:].strip()
			tag520 = '=520  \\\\$a' + summary + '\n'
			fout.write(tag520)
		elif line.strip()[:3] == '510':
			newline = line.split('|')
			for word in newline:
				#original Title 130
				if word[0] == 'a':
					original_title = word[1:].strip()
			tag246 = '=246  31$a' + original_title +'\n'
			fout.write(tag246)

		elif line.strip()[:3] == '600':
			newline = line.split('|')
			hold600 = []
			for word in newline:
				# $a (Topical term)
				if word[0] == 'a':
					personal_topic = '$a' + word[1:].strip()
					hold600.append(personal_topic)
				# v Form subdivision
				elif word[0] == 'c':
					personal_topic_more = '$c' + word[1:].strip()
					hold600.append(personal_topic_more)
				#x general	
				elif word[0] == 'f':
					period_topic = '$d' + word[1:].strip()
					hold600.append(period_topic)
				# z Geographic subdivision
				elif word[0] == 'x':
					theme_topic = '$x' + word[1:].strip()
					hold600.append(theme_topic)
				#$y - Chronological subdivision	
				elif word[0] == 'y':
					geo_topic = '$z' + word[1:].strip()
					hold600.append(geo_topic)
				elif word[0] == 'z':
					period_more_topic = '$y' + word[1:].strip()
					hold600.append(period_more_topic)
			print hold600

			tag600 = '=600  00' + ''.join(hold600) +'\n'
			fout.write(tag600)

		elif line.strip()[:3] == '605':
			newline = line.split('|')
			hold605 = []
			for word in newline:
				if word[0] == 'a':
					subject_Uniform_title = '$a' + word[1:].strip()
					hold605.append(subject_Uniform_title)
				elif word[0] == 'j':
					subject_Uniform_title_Form_subdivision = '$v' + word[1:].strip()
					hold605.append(subject_Uniform_title_Form_subdivision)
				elif word[0] == 'x':
					subject_General_subdivision = '$x' + word[1:].strip()
					hold605.append(subject_General_subdivision)
			tag630 = '=630  \\\\' + ''.join(hold605) +'\n'
			print tag630
			fout.write(tag630)

		elif line.strip()[:3] == '606' or line.strip()[:3] == '607':
			newline = line.split('|')
			hold606 = []
			for word in newline:
				# $a (Topical term)
				if word[0] == 'a':
					subject_topical = '$a' + word[1:].strip()
					hold606.append(subject_topical)
				# v Form subdivision
				elif word[0] == 'j':
					subject_form = '$v' + word[1:].strip()
					hold606.append(subject_form)
				#x general	
				elif word[0] == 'x':
					subject_general = '$x' + word[1:].strip()
					hold606.append(subject_general)
				# z Geographic subdivision
				elif word[0] == 'y':
					subject_geographic = '$z' + word[1:].strip()
					hold606.append(subject_geographic)
				#$y - Chronological subdivision	
				elif word[0] == 'z':
					subject_chronological = '$y' + word[1:].strip()
					hold606.append(subject_chronological)
			print hold606

			tag650 = '=650  \\\\' + ''.join(hold606) +'\n'
			fout.write(tag650)



		elif line.strip()[:3] == '701':
			newline = line.split('|')
			for word in newline:
				#author
				if word[0] == 'a':
					author_local = word[1:].strip()
				elif word[0] == '4':
					author_local_role = word[1:].strip()
				elif word[0] == '9':
					author_local_pinyin = word[1:].strip()
			tag700 = '=700  1\\$a' + author_local + '$e' + author_local_role + '$9' + author_local_pinyin + '\n'
			fout.write(tag700)

		elif line.strip()[:3] == '702':
			newline = line.split('|')
			for word in newline:
				#700 $a (Personal name)Field 700 contains the name of a person who has some responsibility for the content of the item but who cannot be identified as the primary author.
				if word[0] == 'a':
					author_other = word[1:].strip()
				elif word[0] == '4':
					author_other_role = word[1:].strip()
				elif word[0] == '9':
					author_other_pinyin = word[1:].strip()
			tag700 = '=700  1\\$a' + author_other + '$e' + author_other_role + '$9' + author_other_pinyin + '\n'
			fout.write(tag700)

	fin.close()
	fout.close()
	remove_empty_lines('output.txt')
	separet_record('output.txt')


def remove_empty_lines(filename):
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(str.strip, lines)
        filehandle.writelines(lines)
def separet_record(filename):
	with open(filename, "r") as in_file:
		buf = in_file.readlines()
	with open(filename, "w") as out_file:
		for line in buf:
			if line == "=LDR  00000nam a2200000Ia 45e0\n":
				line = "\n" + line
			out_file.write(line)


process_txt('C:\Users\pan.david\Documents\WinPython-64bit-2.7.10.3\marc\input.txt')

#process_txt('C:\Users\pan.david\Documents\WinPython-64bit-2.7.10.3\marc\input.txt')

"""

"""
"""
def walk2(dirname):
    file_dict = dict()
    for root, dirs, files in os.walk(dirname):
        for filename in files:
        	isbn=filename[:13]
        	file_dict[isbn]=os.path.join(root, filename)
    return file_dict

def process_the_whole_dir(dirname):
	dic = walk2(dirname)
	for isbn in dic:
		print dic[isbn]
		process_txt(isbn, dic[isbn])


"""
