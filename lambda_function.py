import json
import boto3
import csv
from math import radians, cos, sin, asin, sqrt
from collections import Counter


# Functon to calculate distance between two coordinates
def haversinepython(lon1, lat1, lon2, lat2):
   
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    
    return c * r
    
def is_present_nyc(lat,long):
    #Checking lat and long are in newyork boundary
    lat_max=40.917577
    lat_min=40.477399
    
    long_max=-73.700009
    long_min=-74.25909
    
    if(lat<lat_min or long>lat_max):
      return False
    if(lat<long_min or long> long_max):
      return False
    return True

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    print(event)
    body = event['messages']
    latitude = float(body["unstructured"]["lat"])
    longitude = float(body["unstructured"]["long"])
    print(latitude)
    print(longitude)
    
    if is_present_nyc(latitude,longitude) == False :
        
        return {
        'statusCode': 200,
        'body': json.dumps('Your location is not in the limits of NYC')
        }
    
        
    
    
    
    # reading data from s3 bucke
    data = s3.get_object(Bucket='nyccrimedata', Key='crimedata.csv')
    threshold = s3.get_object(Bucket='nyccrimedata', Key='crimeThreshold.csv')
    reader = csv.reader(threshold['Body'].read().decode('utf-8').splitlines())
    contents = data['Body'].read().decode('utf-8').splitlines()
    # building threshold dictionary for different ADDR_PCT_CD
    thresholddict = {}
    for row in reader:
       k, v = row
       thresholddict[k] = v
    list = []
    # to know which ADDR_PCT_CD will all matched latitude and longitudes calculated in a mile 
    thresholdArea = []
    
    for row in contents:
        rowSplit = row.split(',')
        # calculates distance for each row with our current coordinates -- for now current coordinates hard coded
        distance = haversinepython(float(rowSplit[6]),float(rowSplit[5]),longitude,latitude)
        # checks whether corresponding lat and long are in a mile or not
        if (distance>=0) & (distance<=1):
            thresholdArea.append(rowSplit[2])
            list.append(rowSplit[4])
    # calculates mean of threshold from all possible thresholds in the above declared set where lat and long fall within a mile
    thresholdAreadict = Counter(thresholdArea)
    rankThresholdArea = {key: rank for rank, key in enumerate(sorted(thresholdAreadict, key=thresholdAreadict.get, reverse=False), 1)}
    count = 0 
    countThreshold = 0
    for x in thresholdAreadict.keys():
        count = count + int(thresholddict[x]) * rankThresholdArea[x]
    if len(thresholdAreadict) >0 :
        countThreshold = count/sum(rankThresholdArea.values())
    # prints total number of rows in a mile
    print(len(list))
    dict = {}
    dict = Counter(list)
    
    # calculating total crimes in a mile
    crimesum = dict['FELONY']*3 + dict['MISDEMEANOR'] * 2 + dict['VIOLATION'] * 1
    # Evaluating area safe or not by comparing above calculated crimes with threshold
    SafetyLevel = ''
    if (crimesum > (0.75 * countThreshold)) :
        SafetyLevel = "unsafe"
        print('unsafe')
    elif (crimesum > (0.50 * countThreshold)) :
        SafetyLevel = 'Moderate Safe'
        print('moderate safe')
    else :
        SafetyLevel = 'Safe'
        print('safe')
   
    return {
        'statusCode': 200,
        'body': json.dumps({'SafetyLevel' : SafetyLevel,'CrimeReport' : dict})
    }
