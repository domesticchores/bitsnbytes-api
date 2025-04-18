# Bits 'n Bytes API

API for Bits 'n Bytes, a Computer Science House Imagine project. 

# Local Development

## Install Python Requirements
1. Create a virtual environment using the following command:
```
python3 -m venv .venv
```
2. Activate the virtual environment using:
```
Linux / Mac:
source .venv/bin/activate

Windows:
cd .venv/Scripts/ 
activate.bat
```
3. Install requirements:
```
pip install -r requirements.txt
```
4. Start the application:
```
python app.py
```

## Configure Environment Variables

### General 
Any environment variables can be added by editing the `config.env.py` file. you can change the defaults or run a `.env` file.
- At minimum, `DB` credentials, `IP`, and `PORT` are needed to run the application.
- Add `S3` credentials for image management when working with users
- To prevents CORS errors when connecting to the front end when testing, add the development URL as `BNB_WEBSITE`

### Windows Specific
If you're like me and running windows for some reason, you can create an `env.bat` file that must be run before starting the application.
- Each variable should be on its own line, following the syntax:
```
...
SET BNB_WEBSITE=http://localhost:3000
...
```
- Then, using `cmd`, run the following when starting the application:
```
call env.bat && python app.py
```