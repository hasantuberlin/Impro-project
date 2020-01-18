import pprint
import re
import json
from datetime import datetime
import sys

def addToICD9List(listValues):
	#print(listValues)
	ICD9Dict= {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
		'dd': listValues[2].split('=')[1],
		'ds':int(listValues[3].split('=')[1]),
		'ld':listValues[4].rstrip().split('=')[1],
	}
	return ICD9Dict

def addToMedicationEventList(listValues):
	medicationEventDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		medicationEventDict[key] = val
	return medicationEventDict
	
def addToAdditiveList(listValues):
	additiveDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		additiveDict[key] = val
	return additiveDict

def addToDeliveryList(listValues):
	deliveryDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		deliveryDict[key] = val
	return deliveryDict

def addToCensusEventList(listValues):
	censusEventDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		censusEventDict[key] = val
	return censusEventDict

def addToTotalIOEventList(listValues):
	totalIOEventDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		totalIOEventDict[key] = val
	return totalIOEventDict

def addToSolutionList(listValues):
	solutionDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		solutionDict[key] = val
	return solutionDict

def addToIOEventList(listValues):
	ioEventDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		ioEventDict[key] = val
	return ioEventDict

def addToPhysicianOrderList(listValues):
	physicianOrderDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		physicianOrderDict[key] = val
	return physicianOrderDict

def addToChartEventList(listValues):
	chartEventDict = {
		'date': listValues[0].strip('[]'),
		'source': listValues[1],
	}
	for no in range(2,len(listValues)):
		key = listValues[no].split('=')[0]
		val = listValues[no].rstrip().split('=')[1].strip('[]')
		chartEventDict[key] = val
	return chartEventDict





# input wavedata is a list which carrys all rows as dictionary 
# read the given wave data from file. read each line and create a dict for each line. 
# then add them into waveData List
def getWaveData(filePath, waveData):

	with open (filePath) as file: # opening file
		noOfLine=1 # as 1st 2 line
		headers=[]
		lineBreak = 0 
		for line in file:
			if(noOfLine > 2):       # reading the value
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
				waveData.append(wavefromDict)
				lineBreak+=1
				if (lineBreak > 5):
					break
				noOfLine +=1

			elif(noOfLine == 2):     # reading 2nd line. which is unit of each value.
				noOfLine += 1
				continue
		
			elif(noOfLine == 1):   # header 
				noOfLine += 1
				headers = line.rstrip().split(',')
			else:
				noOfLine += 1

		return waveData

def getClinicalData(filePath, clinicalDataDict):
	clinicalData = {
					'medicationEvent': list(),
					'physicianOrder': list(),
					'solution': list(),
					'totalIOEvent': list(),
					'IOEvent': list(),
					'ICD9': list(),
					'additive': list(),
					'censusEvent': list(),
					'chartEvent': list(),
					'Delivery': list()
					}
	medicationEventList=[] 
	physicianOrderList=[]
	solutionList=[]
	totalIOEventList=[]
	IOEventList=[]
	ICD9List=[]
	additiveList=[]
	censusEventList=[]
	chartEventList=[]
	deliveryList=[]

	with open (filePath) as file: # opening file
		for line in file:
			words= line.split('\t')

			if(words[1] =='me'):  # checking for each source and then adding them in dict
				continue
				medicationEventList.append(addToMedicationEventList(words))
				#continue
			elif(words[1] == 'wf'): ############ NOT IMPLEMENTED ################
				print(words)

			elif(words[1] == 'ch'): # too much value will work on it later ############ NOT IMPLEMENTED ################
				#print(len(words), words)
				continue
				chartEventList.append(addToChartEventList(words))
				#continue		

			elif(words[1] == 'ad'):
				continue
				additiveList.append(addToAdditiveList(words))

			elif(words[1] == 'de'):
				#print(len(words), words)
				continue
				deliveryList.append(addToDeliveryList(words))

			elif(words[1] == 'ce'):
				#print(len(words), words)
				continue
				censusEventList.append(addToCensusEventList(words))

			elif(words[1] == 'to'): 
				#print(len(words), words)
				continue
				totalIOEventList.append(addToTotalIOEventList(words))
			
			elif(words[1] == 'so'): ############ NOT IMPLEMENTED 
				#print(len(words), words)
				continue
				solutionList.append(addToSolutionList(words))

			elif(words[1] == 'io'): ############ NOT IMPLEMENTED 
				#print(len(words), words)
				continue
				IOEventList.append(addToIOEventList(words))
			
			elif(words[1] == 'ic'): 
				#print(len(words), words)
				ICD9List.append(addToICD9List(words))

			elif(words[1] == 'po'): ############ NOT IMPLEMENTED  
				#print(len(words), words)
				continue
				physicianOrderList.append(addToPhysicianOrderList(words))

			elif(words[1] == 'nu'): ############ NOT IMPLEMENTED ################
				print(words)
			else:
				continue
		clinicalDataDict = {
					'medicationEvent': medicationEventList,
					'physicianOrder': physicianOrderList,
					'solution': solutionList,
					'totalIOEvent': totalIOEventList,
					'IOEvent': IOEventList,
					'ICD9': ICD9List,
					'additive': additiveList,
					'censusEvent': censusEventList,
					'chartEvent': chartEventList,
					'Delivery': deliveryList
					}
	return clinicalDataDict 

def main():


	patient= dict()
	patient['subID']= 's00318'
	patient['sex']= 'm'
	patient['age']= 12
	patient['dateOfBirth']= '13/02/03'

	wfData = getWaveData('a40012n.csv', list())
	patient['wafeData'] = wfData
	clData = getClinicalData('s00318.txt', dict()) 
	patient['clinicalData'] = clData
	


	with open('wave_clinical_partof_fulldata.json', 'w') as f:
		json.dump(patient, f, ensure_ascii=False, indent=4)
	
	pp = pprint.PrettyPrinter(indent=4)
	print("WAVEFROM DATA")
	pp.pprint(patient)


if __name__ == '__main__':
	main()