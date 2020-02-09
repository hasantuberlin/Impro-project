'''
each line from the input file creates a dictionary. then all of them are sent to saved as a json file.  
'''


import pprint
import re
import json
from datetime import datetime
import sys



'''
open waveform data and then convert each line to dictionary and then add them to list. 
return list 
'''

def getWaveData(path: str, cId: str) -> list:
	print('processing Wave Data')
	waveDataList = []
	with open(path) as file:
		headers = []
		for i, line in enumerate(file):
			if(i > 1):       # reading the value
				words = line.rstrip().split(',')
				wavefromDict = dict()
				for i in range(0, len(words)):
					key = headers[i].strip("'")
					value = '-1.000' if words[i] == '-' else words[i].strip("'[]") # in data field some values are replaced by - . so sendng -1 for that
					# in above also stripping ' and [ and ] from data. 
					value = value if '/' in value else float(value) # only date is date type. other will be float type in our data
					#below line with datetime format. but dont work whn we try to serialize the data. 
					#value = datetime.strptime(value, '%H:%M:%S %d/%m/%Y') if '/' in value else float(value) # only date is date type. other will be float type in our data
					wavefromDict[key] = value	
				wavefromDict['source'] = 'wf'
				wavefromDict['wid'] = path.split('/')[-1].split('.')[0]
				wavefromDict['cid'] = cId
				waveDataList.append(wavefromDict)
		
			elif(i == 0):   # header 
				headers = line.rstrip().split(',')
			else:
				continue


		return waveDataList


'''
open clinical data and then convert each line to dictionary and then add them to list. 
return list 
'''
def getClinicalData(path: str) -> list:
	print('processing clinical Data')
	clDataList = []
	cId = path.split('/')[-1].split('.')[0]
	with open(path) as file:
		for line in file:
			words = line.split('\t')
			clDict = {}
			clDict['cid'] = cId
			clDict['Time and date'] = words[0].strip('[]')
			clDict['source'] = 'cl'
			clDict['subSource'] = 'cl-' + words[1]
			for no in range(2,len(words)):
				key = words[no].split('=')[0]
				val = words[no].rstrip().split('=')[1].strip('[]')
				clDict[key] = val
			clDataList.append(clDict)
	return clDataList


'''
write data into writePath
'''
def writeData(writePath, data):
	print('Writing Data to ',writePath)
	with open(writePath, 'w') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)
	print ('success')


'''
convert clinical and waveform data to json file
'''
def loadData(writePath, clinicalDataPath, *webFormDataPath):
	totalDataList = [] # save all data. 

	cId= clinicalDataPath.split('/')[-1].split('.')[0] # findinf clinical Id 
	clDataList = getClinicalData(clinicalDataPath) # return list of json doc
	totalDataList.extend(clDataList)

	for path in webFormDataPath:
		totalDataList.extend(getWaveData(path,cId))

	#print(len(totalDataList))
	writeData(writePath, totalDataList)

'''
convert MAP data to json file
'''
def loadMapper(writePath,filePath):
	recordList = []
	with open (filePath) as file: 
		for i, line in enumerate(file):
			if 'Notes:' in line: # breaking when no useful value is there.
				break
			if i >1: #discarging 1st 2 lines . headers
				words = line.rstrip().split('\t')
		
				if len(words) is 6: # only taking full values. 
					recordDict= {}
					recordDict['ClRecordID']= words[0]
					recordDict['WfRecordID']= words[1]
					recordDict['Sex']= words[2]
					recordDict['Age']= words[3]
					recordDict['Birthdate']= words[4]
					recordDict['wfRecordDate'] = words[5] 	
					print(recordDict)
					recordList.append(recordDict)
	writeData(writePath, recordList)


'''
convert dictionary data to json file
'''
def loadDictionaryData(writePath, filePath):  # file names cg-dict, ch-id-dict,  
	idDict = {}

	with open (filePath) as file: 
		for i, line in enumerate(file):
			words = line.rstrip().split('\t')
			if(i>0) and (len(words)>1): # first line can be header so deal below, id can be null. 
				idDict[words[0]] = words[1]
				#print(words)
			elif (i==0): # checkin 1st line
				print(words)
				if 'id' in words: # discarding header filefound 1st line
					continue
				else :
					idDict[words[0]] = words[1]
			elif (len(words)==1): # only one value in the line. id is null
				idDict[words[0]] = ''

	writeData(writePath, idDict)





def main():

	loadData('a12.json', 's00318.txt', 'a40012n.csv') # convert clinical and waveform data
	loadMapper('map.json','MAP')
	loadDictionaryData('ch-id-dict.json','ch-id-dict')
 



if __name__ == '__main__':
	main()