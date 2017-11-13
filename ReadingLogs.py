#!/usr/bin/python

import time
import glob
import os
import re
import win32security
import ntsecuritycon as con
import pdb
from pathlib import Path

# userx, domain, type = win32security.LookupAccountName("", "Everyone")
cleanpath1 = os.path.expanduser('~/Desktop/')
# change this folder to the folder with the logs
folder = Path(os.path.expanduser('~\Documents\logs\PA1'))


# outputWarn = open(warnPath, 'a')
# outputError = open(errorPath, 'a')
# outputFatal = open(fatalPath, 'a')


def main():
    os.umask(000)
    readWriteLogs(folder)
    # getDuplicates(outfolder, 'warn')
    # getDuplicates(outfolder, 'error')


def getDuplicates(file, name):
    lines = open(file, 'rb').readlines()
    lines_set = set(lines)
    out = open(file + name + 'Clean.txt', 'wb')

    for line in lines_set:
        out.write(line)

    print("Done filtering on duplicates of " + name)
    out.close()


def readWriteLogs(folder):
    # folder = Path(os.path.expanduser('~\Documents\Logs_PA2_After\Logs'))
    name_folder = folder.parts[5]
    # print(folderName)

    for filename in glob.iglob(os.path.join(folder, '*')):
        try:
            outfolder = cleanpath1 + '/' + name_folder
            os.makedirs(outfolder)

        except OSError:
            if not os.path.isdir(outfolder):
                raise

    outputWarn = open(outfolder + '/warn.txt', 'wb')
    outputError = open(outfolder + '/error.txt', 'wb')
    outputFatal = open(outfolder + '/fatal.txt', 'wb')

    for filename in glob.iglob(os.path.join(folder, '*')):
        with open(filename, encoding='utf-8-sig') as f:
            # with open(filename) as f:
            # print(filename + "%s\n"% filename.encode('utf-8'))
            # One file open, handle it, next loop will present you with a new file.
            print(filename.encode("utf-8-sig"))
            for line in f:
                # Change datum if needed.
                matchWarn = re.match(r'.*2017-10-27.*WARN.*', line)
                matchError = re.match(r'.*2017-10-27.*ERROR.*', line)
                matchFatal = re.match(r'.*2017-10-27.*FATAL.*', line)

                if matchFatal:
                    outputFatal.write(line.encode())
                elif matchError:
                    outputError.write(line.encode())
                elif matchWarn:
                    outputWarn.write(line.encode())

    getDuplicates(outfolder + '/warn.txt', 'warn')
    getDuplicates(outfolder + '/error.txt', 'error')

    f.close()
    outputWarn.close()
    outputError.close()
    outputFatal.close()

def deleteStamp(path):
    with open("C:\\Users\\Administrator\\Documents\\test1.txt", 'wb', encoding="utf-8-sig") as outputfile:
        with open(path, encoding='utf-8-sig') as f:
            for line in f:
                newLine = line.replace(line[:23], "")
                # print(newLine)
                outputfile.write(newLine)

    outputfile.close()

def tijs():
	print (' -------------------------------')
	print ('|     Application Started       |')
	print (' -------------------------------')

	# Set date/time parsing | leave empty for no parsing #
	#regexTime = re.compile(r'.*2014-11-05.*')
	regexTime = re.compile(r'.*')

	#Set log level to parse | DEBUG, ERROR, WARN, FATAL, INFO #
	regexErrors = re.compile(r'.*WARN|ERROR|FATAL.*')

	# Set paths to logs, results and the file containing the regular expressions #
	path = r'C:\Users\Administrator\Desktop\PA1'
	resultpath = r'C:\Python\results'
	f = open(r'C:\Python\Regex.txt')

	# Clean results directory #
	print ('1. Cleaning results directory')
	for the_file in os.listdir(resultpath):
		file_path = os.path.join(resultpath, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print (e)

	# Read all regular expressions and insert into an array #
	print ('2. Calculating number of regular expressions')
	allRegex = []
	for line in f:
		allRegex.append(re.compile(line))

	nrRegex = len(allRegex)
	print ('- Number of regular expressions: ' + str(nrRegex))
			
	# Parse the log files based on date/time and log level; this is written to ".new" file in the result path #
	logFiles = os.listdir(path)
	nrFiles = len(logFiles)
	print ('3. Parsing ' + str(nrFiles) + ' file(s) based on date/time and log level')
	atFile = 0
	print ('- 0.00%')
	for filename in logFiles:
		atFile += 1
		log = os.path.join(path, filename)
		resultlog = os.path.join(resultpath, filename)
		fin = open(log, "r")
		fout = open(resultlog + '.new', 'w')
		for line in fin:
			if regexTime.findall(line):
				if regexErrors.findall(line):
					fout.write(line)
		fin.close()
		fout.close()
		print ('- ' + ("%.2f" % (float(atFile)*100/float(nrFiles))) + '%')

	# Start parsing all files in the result path, this should only contain ".new" files before the parsing #
	# For each ".new" file a leftover file will be created with all messages that could not be parsed based on the regular expressions #
	# For each regular expression that has a match in the ".new" file a new file will be created containing all messages for this specific regular expression (index in the extension) #
	logFiles = os.listdir(resultpath)
	nrFiles = len(logFiles)
	print ('4. Parsing ' + str(nrFiles) + ' file(s) based on regular expressions')
	atFile = 0
	print ('- 0.00%')
	for filename in logFiles:
		atFile += 1
		log = os.path.join(resultpath, filename)	
		fleftover = open(log + '.leftover', 'w')
		fin = open(log, "r")
		countErrors=[]
		for y in range(nrRegex):
			countErrors.append(0)
		fouterrors=[]
		for x in range(nrRegex):
			fouterrors.append(log + '.errors_' + str(x+1))
		for line in fin:
			i=0
			found=0
			line2 = line
			for regex in allRegex:
				if regex.findall(line):
					countErrors[i]+=1
					fouterror = open(fouterrors[i], 'a')
					fouterror.write(line2)
					fouterror.close()
					i=0
					found = 1
					break
				else:
					i+=1
			if found == 0:
				fleftover.write(line)
			
		fin.close()	
		fleftover.close()
		print ('- ' + ("%.2f" % (float(atFile)*100/float(nrFiles))) + '%')
		
		# Write results to a separate ".result" file for each ".new" file #
		print ('5. Writing results')
		fout = open(log + '.result', 'w')
		print ('- 0.00%')
		for y in range(nrRegex):
			if countErrors[y] != 0:
				fout.write(str(countErrors[y]) + ' ' + allRegex[y].pattern)
				print ('- ' + ("%.2f" % (float(y+1)*100/float(nrRegex))) + '%')
		fout.close()

	print ('6. Finishing application')
	print (' -------------------------------')
	print ('|    Application Finished       |')
	print (' -------------------------------')

if __name__ == "__main__":
    # execute only if run as a script

    main()