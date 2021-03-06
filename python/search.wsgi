#!/usr/local/bin/python

import MySQLdb
import cgi
import json
import datetime
import re

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

KEY_STR = 'umprojkey6853558'

def application(environ, start_response):
    
    #get proper fields
    form = cgi.FieldStorage(fp=environ['wsgi.input'],
                            environ=environ,
                            keep_blank_values=True)
    
    userid = form.getfirst('userid','empty')
    ethnicity = form.getfirst('ethnicity', 'empty')
    ethnicity = cgi.escape(ethnicity)
    nationality = form.getfirst('Birth_Country', 'empty')
    nationality = cgi.escape(nationality)
    city = form.getfirst('city', 'empty')
    city = cgi.escape(city)
    gender = form.getfirst('gender', 'empty')
    gender = cgi.escape(gender)
    pref = form.getfirst('orientation', 'empty')
    pref = cgi.escape(pref)
    minAge = form.getfirst('minAge', 'empty')
    minAge = cgi.escape(minAge)
    maxAge = form.getfirst('maxAge', 'empty')
    maxAge = cgi.escape(maxAge)
    sort = form.getfirst('sort', 'empty')
    sort = cgi.escape(sort)
    sortOrder = form.getfirst('sortOrder', 'empty')
    sortOrder = cgi.escape(sortOrder)

    #Awful code that converts what we get into SQL parameters. Very dangerous for SQL injection
    if sort == "Name":
    	sort = 'User_Name'
    
    if gender == "Men":
    	gender = "SEX = 'M'"
    
    if gender == "Women":
    	gender = "SEX = 'F'"
    
    if gender == "Men/Women":
    	gender = "(SEX = 'F' OR SEX = 'M')"
    
    if pref == "Men":
    	pref = "orientation = 'M'"
    
    if pref == "Women":
    	pref = "orientation = 'F'"
   
    if pref == "Men/Women":
    	pref = "(orientation = 'F' OR orientation = 'M')"
    	
    #What we want to do: Take NOW and minus minBirthDate years and save it
    #then take NOW and minus maxBirthDate years and save it
    now = datetime.date.today()
       
    minAge = int(minAge)
    maxAge = int(maxAge)
    
    #Takes todays date and minuses the years (365 * year) and spits out in proper format - yyyy-mm-dd
    minBirthDate = (now - datetime.timedelta(maxAge*365)).isoformat()
    maxBirthDate = (now - datetime.timedelta(minAge*365)).isoformat()    	
        
    ethnicityCmd = "Ethinicity = '"+ethnicity+"'"
    nationalityCmd = "Birth_Country = '"+nationality+"'"
    cityCmd = "City = '"+city+"'"
    
    #connect to the Database
    conn = MySQLdb.connect (host = "localhost",
                            user = "root",
                            passwd = "",
                            db = "campus chemistry")

    cursor = conn.cursor()
    
    #UGH, BFI method. Horrible horrible coding.
  	
    filterPref = "SELECT User_Name, Department, User_ID, Body_type, About_Me, Profile_Picture, Email_ID FROM user_profile WHERE Email_ID != '" + userid + "' AND " + ethnicityCmd + " AND " + nationalityCmd + " AND " + cityCmd + " AND " + gender + " AND " + pref + " AND DOB BETWEEN '" + minBirthDate + "' AND '" + maxBirthDate + "' ORDER BY " + sort + " " + sortOrder 
  	
    if ethnicity == "Any" and nationality == "Any" and city == "Any":
        filterPref = "SELECT User_Name, Department, User_ID, Body_type, About_Me, Profile_Picture, Email_ID FROM user_profile WHERE Email_ID != '" + userid + "' AND " + gender + " AND " + pref + " AND DOB BETWEEN '" + minBirthDate + "' AND '" + maxBirthDate + "' ORDER BY " + sort + " " + sortOrder                
    elif ethnicity == "Any" and nationality != "Any" and city == "Any":
        filterPref = "SELECT User_Name, Department, User_ID, Body_type, About_Me, Profile_Picture, Email_ID FROM user_profile WHERE Email_ID != '" + userid + "' AND " + nationalityCmd + " AND " + gender + " AND " + pref + " AND DOB BETWEEN '" + minBirthDate + "' AND '" + maxBirthDate + "' ORDER BY " + sort + " " + sortOrder
    elif ethnicity != "Any" and nationality == "Any" and city == "Any":
        filterPref = "SELECT User_Name, Department, User_ID, Body_type, About_Me, Profile_Picture, Email_ID FROM user_profile WHERE Email_ID != '" + userid + "' AND " + ethnicityCmd + " AND " + gender + " AND " + pref + " AND DOB BETWEEN '" + minBirthDate + "' AND '" + maxBirthDate + "' ORDER BY " + sort + " " + sortOrder
    elif ethnicity == "Any" and nationality == "Any" and city != "Any":
        filterPref = "SELECT User_Name, Department, User_ID, Body_type, About_Me, Profile_Picture, Email_ID FROM user_profile WHERE Email_ID != '" + userid + "' AND " + cityCmd + " AND " + gender + " AND " + pref + " AND DOB BETWEEN '" + minBirthDate + "' AND '" + maxBirthDate + "' ORDER BY " + sort + " " + sortOrder    
    elif ethnicity != "Any" and nationality != "Any" and city == "Any":
        filterPref = "SELECT User_Name, Department, User_ID, Body_type, About_Me, Profile_Picture, Email_ID FROM user_profile WHERE Email_ID != '" + userid + "' AND " + ethnicityCmd + " AND " + nationalityCmd + " AND " + gender + " AND " + pref + " AND DOB BETWEEN '" + minBirthDate + "' AND '" + maxBirthDate + "' ORDER BY " + sort + " " + sortOrder
    elif ethnicity != "Any" and nationality == "Any" and city != "Any":
        filterPref = "SELECT User_Name, Department, User_ID, Body_type, About_Me, Profile_Picture, Email_ID FROM user_profile WHERE Email_ID != '" + userid + "' AND " + ethnicityCmd + " AND " + cityCmd + " AND " + gender + " AND " + pref + " AND DOB BETWEEN '" + minBirthDate + "' AND '" + maxBirthDate + "' ORDER BY " + sort + " " + sortOrder    
    elif ethnicity == "Any" and nationality != "Any" and city != "Any":
        filterPref = "SELECT User_Name, Department, User_ID, Body_type, About_Me, Profile_Picture, Email_ID FROM user_profile WHERE Email_ID != '" + userid + "' AND " + nationalityCmd + " AND " + cityCmd + " AND " + gender + " AND " + pref + " AND DOB BETWEEN '" + minBirthDate + "' AND '" + maxBirthDate + "' ORDER BY " + sort + " " + sortOrder                
        
    cursor.execute(filterPref)
    
    rows = cursor.fetchall()
    names = []
    departments = []
    ids = []
    types = []
    abouts = []
    pictures = []
    emails = []

    for row in rows:
        names.append(row[0])
        departments.append(row[1])
        ids.append(row[2])
        types.append(row[3])
        abouts.append(row[4])
        pictures.append(row[5])
        emails.append(row[6])
        
    results = []
    for i in range(0,len(names)):
        results.append({"name":names[i], "department": departments[i], "id": ids[i], "type":types[i], "about":abouts[i], "picture":pictures[i],"email":emails[i] })
     
    output = json.dumps(results)

    status = '200 OK'

    cursor.close()
    conn.commit()
    conn.close()

    response_headers = [('Content-Type', 'application/json'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]