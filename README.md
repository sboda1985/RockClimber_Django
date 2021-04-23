# RockClimber_Django

RockClimber is an app designed to log your climbed routes/walls/regions
<br/><br/>

Requests should be sent to https://bodaszilard.hopto.org/rockclimber/ <br/>
entering the appropiate module, like:  https://bodaszilard.hopto.org/rockclimber/checklogin/<br/>
<br/><br/>
The following modules are done now:<br/>

    addwall
    checklogin
    forgotpassword
    registration
    resetpasswordwithpin

## addwall
<br/><br/>
Adds a wall to the database in a specific region<br/>
<br/>
URL: https://bodaszilard.hopto.org/rockclimber/addwall/<br/>
Request: POST<br/>
Parameters:<br/>
user_id - the id of the user<br/>
pin - the pin of the logged in user<br/>
region - the name of the region in which the wall exists<br/>
wallname<br/>
walldescription<br/>
wallapproach<br/>
wallaccess<br/>
route_quality<br/>
popularity<br/>
note<br/>
<br/><br/>
Output:<br/>
"wall":"added" - if the adding was successfull<br/>
"wall":"exists" - if there is a wall with a matching name in that region<br/>
"Region":"does not exists" - if such region does not exists<br/>


## checklogin
<br/><br/>
Checks whether the entered password matches the one in the database<br/>
URL: https://bodaszilard.hopto.org/rockclimber/checklogin/<br/>
Request: POST<br/>
Parameters:<br/>
email - the email of the registered user<br/>
password - the password of the user<br/>

<br/><br/>
Output:<br/>
'match':'false - to many attempts, wait a day' - if there seems to be a brute force guessing of the password<br/>
'match':'true','pin':pin - if the entered password was a match<br/>
'match':'false' - if the password does not match<br/>


## forgotpassword - currently not working
<br/><br/>
sends an email with a PIN to reset the password<br/>
<br/>
URL: https://bodaszilard.hopto.org/rockclimber/forgotpassword/<br/>
Request: POST<br/>
Parameters:<br/>
email - the registered email address<br/>

<br/><br/>
Output:<br/>
'email':'not registered' - if there is no such email address<br/>
'forgot':'reset email sent', 'id':id - if the email exists<br/>


## resetpasswordwithpin

resets the password
<br/><br/>
URL: https://bodaszilard.hopto.org/rockclimber/resetpasswordwithpin/<br/>
Request: POST<br/>
Parameters:<br/>
id - id of the user<br/>
pin - pin of the user<br/>
typpass - new password<br/>
<br/><br/>
Output:<br/>
'password_reset':'false - to many attempts, wait a day' - if there is a brute force attack to try to reset the password<br/>
'reset passwrod':'password recovery not requested' - if pin does not match<br/>
'password reset':'success' - if the request was successfull<br/>

