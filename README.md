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


# Using the API

The three endpoints are as follows:
```
{API_ENDPOINT}/add_interactions
{API_ENDPOINT}/add_visions
{API_ENDPOINT}/add_weights
```

The content is passed in as JSON in the request body, that should be fairly easy to set up with the `requests` library in python.
The format for all of them are pretty self explanatory, but its a json [] array with comma separated {} entries like follows:

```
[
    {
        "time": "2025-04-18 20:51:30.091093",
        "slot_id": 1,
        "weight_grams": 1.50
    },
    {
        "time": "2025-04-18 20:53:28.091093",
        "slot_id": 1,
        "weight_grams": -1.50
    }
]
```

This is an example for `add_weights`, but it shows off basically how to do all of them.
If successful, the API returns a `200 OK` with a content body of how many entries added, otherwise it returns a debug error.

To get the training data, which currently only contains `weight` and `vision` data, you use the endpoint below as a `GET` request:
```
{API_ENDPOINT}/training/2025-04-17 20:51:30.091093~2025-04-19 20:51:30.091093
```
The arguments follows the format `START_TIME_STAMP~END_TIME_STAMP` , where both timestamps are formatted as ` %Y-%m-%d %H:%M:%S.%f ` in python. The best way to format this in python is to use the `datetime` libarary.
To create a new date for the entry, simply use `datetime.datetime.now()` which should be automatically formatted for this. make sure that it is passed in as a string, which can be achieved with `datetime.datetime.strftime({DATETIME_OBJECT}, "%Y-%m-%d %H:%M:%S.%f"))`
Make sure that, when passing in the two dates as strings, that there is a `~` symbol between them with no spaces. This is how the API separates the two dates.

On success, the data is returned as a JSON array with two sections, `vision` and `weight`, like the example below:
```
{
  "vision": [
    {
      "vision_class": "CLASS",
      "confidence": 0.0,
      "time": "2025-04-18 16:51:36.020093"
    },
    {
      "vision_class": "CLASS",
      "confidence": 0.5,
      "time": "2025-04-18 20:51:30.091093"
    },
    {
      "vision_class": "CLASS",
      "confidence": 0.75,
      "time": "2025-04-18 20:53:28.091093"
    }
  ],
  "weight": [
    {
      "slot_id": "1",
      "weight_grams": 1.5,
      "time": "2025-04-18 20:51:30.091093"
    },
    {
      "slot_id": "1",
      "weight_grams": -1.5,
      "time": "2025-04-18 20:53:28.091093"
    }
  ]
}
```

If no entries exist for either vision or weight, then the API returns a `404 NOT FOUND` with the status text of `NO RECORDS FOUND FOR {TYPE} DATA`.

If bad timestamps were used, then the API returns a `400 BAD REQUEST` with the status text of `BAD PARAMETERS`.