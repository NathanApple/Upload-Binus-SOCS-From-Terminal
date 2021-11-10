# Upload-Binus-SOCS-From-Terminal
Please star the github project to save the repository
## Instalation
Download and put script.py at working directory ( please put at same folder with the filename that will be uploaded )

[Download python3](https://www.python.org/downloads/).

Make sure following python library already downloaded
- requests
- bs4
- And standard python library 

Recommended, [download window terminal from microsoft store](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701)


## Usage
Open in terminal ( or window terminal )

Put file in any folder ( Note : You are allowed to change the python filename since it doesnt affect anything at all )

Open window terminal / any terminal, 

cd to path

python script.py [filepath] [cid]

example : 
- python script.py C:\SOCS\Task\a.c
- python script.py C:\SOCS\Task\a.c 1
- python script.py C:\SOCS\Task\a.c ?
- python script.py a.c



![Example](https://github.com/NathanApple/Upload-Binus-SOCS-From-Terminal/blob/main/pictures/example1.png?raw=true)


<b>Filepath must be string with following constraint</b>

(path)\(filename).(extension)
<i>or</i>
(filename).(extension)
<i>or</i>
./(filename).(extension)

Path must be string with following constraint
(Parent Drive):\(Folder Path)\(Folder Path)

<b>optional, cid must be string</b>

if cid = ?, it will print all avaible cid to use


## More Info
Discord : Hiko#6357

There will be more update to come, 

Please feel free to ask anything and creating pull request

## Changelog
### Update 1.2
- Fixed a bug when using ? as cid did not update current cid
- Added warning when accessing empty problem cid 

### Update 1.1 
- Now you could upload file in any folder without change current python script folder
- Recent uploaded file path will be saved so when another file needed to be upload, just use the filename without the full path
- Now will get the result live from socs
Update 1.0 First Release
