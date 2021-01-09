# Habitica Todo Reward

This is essentially a copy of the [Double-reward](https://github.com/festeh/Double-reward) project but deployed on Heroku. Like Double-reward, it receives item completion notifications from Todoist via webhook, then creates and completes a Habitica task in response. 

## Notes

| Todoist Priority | Habitica Difficulty |
| :---: | :--- |
| 1 | Hard |
| 2 | Medium |
| 3 | Easy |
| 4 | Easy |

Note: Trivial is not used because I'm lazy and by default Todoist sets all tasks to priority 4. If it's not important it should just be easy, not trivial.

## Deploying to Heroku

General Commands:
```
heroku create <app name> 		# creates an app on heroku at https://<app name>.herokuapp.com/ (only done once)
git push heroku master 			# deploy on heroku
heroku ps:scale web=1			# check that at least one app instance is running
heroku open						# opens the generated url
heroku logs --tail				# view request logs (Crtl+C to quit)
```
Configuring Environment Variables:
```
heroku config 					# lists environment variables
heroku config:get <VAR>			# print value of <VAR>
heroku config:set <VAR>=<value> # add or set <VAR> to <value>
heroku config:unset <VAR>		# remove 
```

### Helpful Links
- [Todoist Python API](https://developer.todoist.com/sync/v8/?python#overview) (not really used)
- [Habitica REST API](https://habitica.com/apidoc/#api-_)
- [festeh/Double-Reward](https://github.com/festeh/Double-reward)
- [Habitica Guidance for Comrades (Rules for 3rd Party Devs)](https://habitica.fandom.com/wiki/Guidance_for_Comrades)
- [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true#set-up)
- [Deploy Python Flask App on Heroku](https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/)

### Acknowledgements

Thank you very much [Dmitry Lipin](https://github.com/festeh) for creating this webhook-based integration between Todoist and Habitica. The majority of my code comes directly from the Double-reward project.