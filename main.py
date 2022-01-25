import urllib3
import json

# OBJECTIVE: create json object for set of sessions by each unique visitor. one session is a group of events with 
# less than 10 minutes between events following the first one. a visitor (marked by visitor id)
# can have multiple sessions

# DATA CONSTRAINT: visitors data can be in any order, timestamps are in milliseconds, 
# generated sessions of visitor must be in chronological, URLs sorted in chronological, 
# duration = 0 when there is only one event in the session

# 600 000 milliseconds = 10 minutes   

def main():
  # allows for requests and keeps track of connection pools
  http = urllib3.PoolManager()

  # get the json data and load it into respDict as a dictionary
  resp = http.request('GET', 'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=fb08086c6c675bd3cf0fa9a8ebc5')
  print(resp.status)
  respDict = json.loads(resp.data)

  sessionDict = {}
  # iterate through all the events
  for singleEvent in respDict["events"]:

    # if the visitor is new, start an array and add an array containing url and timestamp of event to it
    # add the visitor array to sessionDict
    if singleEvent["visitorId"] not in sessionDict.keys():
      visitorArr = []
      visitorArr.append([singleEvent["url"], singleEvent["timestamp"]])
      sessionDict[singleEvent["visitorId"]] = visitorArr
    # else if the visitor has a previous event, update their sessionDict value by adding the new event
    elif singleEvent["visitorId"] in sessionDict.keys():
      dictValArr = sessionDict[singleEvent["visitorId"]]
      dictValArr.append([singleEvent["url"], singleEvent["timestamp"]])
      sessionDict[singleEvent["visitorId"]] = dictValArr

  # iterate through all the users
  for user in sessionDict.keys():
    # sort the user events array by timestamp
    sessionDict[user].sort(key = lambda x:x[1])

    # if a user only has one event, value is updated as follows:
    if len(sessionDict[user]) == 1:
      duration = 0
      pages = [sessionDict[user][0][0]]
      startTime = sessionDict[user][0][1]
      sessionDict[user] = [{
        "duration": duration,
        "pages": pages,
        "startTime": startTime
      }]
    # else if user has multiple events...must separate into sessions...
    elif len(sessionDict[user]) > 1:
      # array for all the sessions of a user
      sessionsArr = []
      # array of a single session
      singleSession = []
      # add the first event of a user into the single session array
      singleSession.append(sessionDict[user][0])

      # simple for loop index iteration
      for eventIndex in range(len(sessionDict[user]) - 1):
        # if the following event is less than or equal to 10 minutes than the last one in the single session, add it to the single session
        if (sessionDict[user][eventIndex + 1][1] - sessionDict[user][eventIndex][1]) <= 600000:
          singleSession.append(sessionDict[user][eventIndex + 1])
        # if the following event is greater than 10 minutes, add this single session to sessions array, clear single session, add following event
        elif (sessionDict[user][eventIndex + 1][1] - sessionDict[user][eventIndex][1]) > 600000:
          sessionsArr.append(singleSession)
          singleSession = []
          singleSession.append(sessionDict[user][eventIndex + 1])
      
      # add the last single session to sessions array
      sessionsArr.append(singleSession)
      # array to hold formatted sessions data
      formattedSessionsArr = []

      # iterate through all the sessions
      for session in sessionsArr:
        # duration is last event timestamp - first event
        duration = session[len(session) - 1][1] - session[0][1]
        # make pages array with all the pages visited in a single session
        pages = []
        for singleEvent in session:
          pages.append(singleEvent[0])
        # startTime is timestamp of the first event
        startTime = session[0][1]
        # format each session and update the users value in sessionDict
        singleSessFormat = {
          "duration": duration,
          "pages": pages,
          "startTime": startTime
        }
        formattedSessionsArr.append(singleSessFormat)
        sessionDict[user] = formattedSessionsArr

  # label the final data, convert to json, POST, check status
  final = {"sessionsByUser":sessionDict}
  toJSON = json.dumps(final)
  resp = http.request('POST', 'https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=fb08086c6c675bd3cf0fa9a8ebc5',
                 headers={'Content-Type': 'application/json'},
                 body=toJSON)
  print(resp.status)


if __name__ == '__main__':
  main()