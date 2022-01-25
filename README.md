# HS_Assessment
python GET, parse, POST json data

## Process to parse visitors log by user sessions 
1. Single ```main.py``` function
2. GET and load data as dictionary
3. Make new dictionary with user as keys and values as array of url+timestamp arrays (or events)
4. Iterate through all the users and sort events by their timestamps to have events be chronological
5. Separate users who only have one event vs multiple
<br /> a. One event users get updated dictionary value immediately
<br /> b. Multiple event users have to have the events separated into single sessions
<br /> &emsp; i. Events in the session are within 10 minutes of each other
<br /> &emsp; ii. Iterate through each session to format it and add it to sessions array and update dictionary user value
6. Label dictionary data and convert to json and POST
7. Print status of POST (should be 200)

## What I Learned
1. It's 2D arrays. Or dictionaries. But mostly 2D arrays. Array? Nah 2D array. 2D arrays everywhere. 
2. It takes as long as it takes ok. 
3. Really though, it's really cool Python lets you sort an array by the array element array element. 
4. json.loads(data) turns json data into python dictionary 
5. json.dumps(data) turns python data into json

## What Was Difficult
If you're still here, look away. You will get stuck with dreams of 2D arrays. Parsing data in 2D arrays. 2D arrays. 2D arrays. 2D arrays. 2D arrays. 2D arrays. 2D arrays. 2D arrays. 2D arrays. 2D arrays. 2D arrays. 2D arrayss. 2D arraysss. 2D arrayssss. 2D arraysssss.

## What's Next
In an ideal world, this code would get optimized. I am pretty sure there's a better way than this. AND less 2D array stuff. But yeah I'll leave it like this now so I can cringe at myself.

## Built Using
VS Code 1.63.2 <br/>
Python3 <br/>
other requirements in ```requirements.txt```
