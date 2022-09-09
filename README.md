# Using Gmail API with Python
This project uses Gmail API to send, search, delete and mark emails as read or unread.

## Getting Started
1. Clone repo & cd into directory
```
git clone https://github.com/AMuriuki/gmail-api-python.git
```
2. Enable Gmail API

    You'll need a token to connect to Gmail's API. First head over to [Google API's dashboard](https://console.developers.google.com/apis/dashboard) to enable the API. 

    Use the search bar to search for `Gmail API`, click on it, then enable it. Create an OAuth 2.0 client ID, click on `Create Credentials` and choose `OAuth Client ID`. 

    Select `Desktop App` as the **Application type** and proceed. Go ahead and download the json file with your client ID & Secret.

    Move the file to the root of your project directory, and rename it to `credentials.json`

3. Create virtual env & activate it (Optional)
```
python3 -m venv venv

. venv/bin/activate
``` 

4. Install required modules
```
pip install -r requirements.txt
```

5. Edit `env.example` accordingly and rename to `.env`
```
email_address="youremail@gmail.com"

# add email recipients seperated by a comma
recipients="someemail@example.com, anotheremail@example.com"
```

6. To send email:
```
python send_email.py
```