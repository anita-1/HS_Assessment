import urllib3
import json

def main():
  # create json object for set of sessions . one session is a group of events with 
  # less than 10 minutes between events following the first one. a visitor (marked by visitor id)
  # can have multiple sessions

  # visitors can be in any order, sessions of visitor must be in chronological, URLs sorted in chronological, duration = 0 when one event

  # 600 000 milliseconds = 10 minutes   

  http = urllib3.PoolManager()

  resp = http.request('GET', 'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=fb08086c6c675bd3cf0fa9a8ebc5')
  print(resp.status)
  respDict = json.loads(resp.data)

  sessionDict = {}
  for eachEvent in respDict["events"]:
    if eachEvent["visitorId"] not in sessionDict.keys():
      visitorArr = []
      visitorArr.append([eachEvent["url"], eachEvent["timestamp"]])
      sessionDict[eachEvent["visitorId"]] = visitorArr
    elif eachEvent["visitorId"] in sessionDict.keys():
      dictValArr = sessionDict[eachEvent["visitorId"]]
      dictValArr.append([eachEvent["url"], eachEvent["timestamp"]])
      sessionDict[eachEvent["visitorId"]] = dictValArr

  
  
  for user in sessionDict.keys():
      sessionDict[user].sort(key = lambda x:x[1])
      if len(sessionDict[user]) == 1:
        duration = 0
        pages = [sessionDict[user][0][0]]
        startTime = sessionDict[user][0][1]
        sessionDict[user] = [{
          "duration": duration,
          "pages": pages,
          "startTime": startTime
        }]
      elif len(sessionDict[user]) > 1:
        
        sessionsArr = []
        eachSession = []
        eachSession.append(sessionDict[user][0])
        for eventIndex in range(len(sessionDict[user]) - 1):
          
          if (sessionDict[user][eventIndex + 1][1] - sessionDict[user][eventIndex][1]) <= 600000:


            eachSession.append(sessionDict[user][eventIndex + 1])

          elif (sessionDict[user][eventIndex + 1][1] - sessionDict[user][eventIndex][1]) > 600000:
            sessionsArr.append(eachSession)
            eachSession = []
            eachSession.append(sessionDict[user][eventIndex + 1])
        sessionsArr.append(eachSession)

        userSessionArr = []

        for session in sessionsArr:

          duration = session[len(session) - 1][1] - session[0][1]

          pages = []
          for eachEvent in session:
            pages.append(eachEvent[0])
          startTime = session[0][1]
          tempSessFormat = {
            "duration": duration,
            "pages": pages,
            "startTime": startTime
          }
          userSessionArr.append(tempSessFormat)
          sessionDict[user] = userSessionArr


  final = {"sessionsByUser":sessionDict}

  toJSON = json.dumps(final)
  
  resp = http.request('POST', 'https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=fb08086c6c675bd3cf0fa9a8ebc5',
                 headers={'Content-Type': 'application/json'},
                 body=toJSON)

  print(resp.status)



if __name__ == '__main__':
  main()