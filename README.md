# Facebook Messenger Bots (Heroku 設定)
Building Facebook Messenger Bots with Python and heroku

## Development Environment Setup
### Tools：
- Language：Python3
- framework：Flask
- Server platform：[Heroku](https://dashboard.heroku.com/)
- [Facebook for Developers](https://developers.facebook.com/)

### Heroku Setup
1. Creat a New APP
Click "New" bottom in the top right corner, and click "Creat new app".
![](https://i.imgur.com/2OuOW3E.png)
<br />
Name the app and click "Create app"
![](https://i.imgur.com/egkRrXw.png)

2. Deploy a Flask app on Heroku
Need **three specific files:**
- requirements.txt
```
git+https://github.com/TheoKlein/PyMessager@master#egg=pymessager
flask
wit
gunicorn==19.6.0
```

- Procfile
`web: gunicorn app:app --log-file=-`

- runtime.txt**
`python-3.6.4`


3. Use Heroku CLI
This page is in Deploy.
![](https://i.imgur.com/mk3RQJ1.png)

### Set Environment Variables in Heroku
- Heroku: Settings -> Config Vars
![](https://i.imgur.com/J7tOOIf.png)

- In Code
```python = 1
import os

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

WIT_ACCESS_TOKEN = os.getenv('WIT_ACCESS_TOKEN')

```

### Deploy
If you already connected your Heroku Project to GitHub

1. Push code to GitHub
`git push origin master`

2. Heroku will build the project automatically.



### Reference
[Tutorial](https://www.twilio.com/blog/2018/02/facebook-messenger-bot-heroku-python-flask.html)





