# vandrApp
This is the stripped-down version of a webapp to encourage people to participate in political campaigning ("gamifying political campaigning"). It allows people to sign up, collect points for achieving different tasks, and compete with other users.

We provide this code here as inspiration for others on how to set up a flask-based webapp of this kind. May it be useful!

## Requirements
The webapp is built on top of flask. Amongst others, it uses auth0 for logins, sql-alchemy for connecting to a database and pandas and seaborn for visualization.
See the [requirements.txt](requirements.txt) for details.

Note: To run a fully-functional version of this app you need to set up accounts with auth0 (https://auth0.com/) for user-authentification and heroku (https://www.heroku.com/) for hosting the app and tweak the configuration of the app such that all the domain names etc match your accounts with these services.

## Running it locally 
To open the app under http://127.0.0.1:5000
	
	python runserver.py
	
## Deploying to Heroku
It's easier than thought! After setting it up (see https://blakeboswell.github.io/article/2016/03/15/heroku-app-template.html), deploying can be as easy as
	
	git push heroku master
	

## References
Flask Web Development by Miguel Grinberg (O'Reilly 2014)


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
