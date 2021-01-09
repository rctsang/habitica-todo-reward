# credit https://github.com/festeh/Double-reward

from os import environ
import requests

# generate authorization header from environment variables (requires dotenv)
def create_habitica_auth_headers():
	uid = environ["HABITICA_USER_ID"]
	token = environ["HABITICA_API_TOKEN"]
	headers = {
		"x-client": f"{uid}-habitica_todoist_rewards",
		"x-api-key": token,
		"x-api-user": uid
	}
	return headers

# creates a habitica task with given priority (default easy) and returns created task id
def create_habitica_task(auth_headers, text, priority="1"):
	create_task_url = "https://habitica.com/api/v3/tasks/user"
	task = {"type": "todo", "text": text, "priority": priority}
	res = requests.post(create_task_url, json=task, headers=auth_headers).json()
	if res['success'] is True:
		data = res['data']
		return data["id"]
	return None

# deletes habitica task with task id
def delete_habitica_task(auth_headers, task_id):
	delete_task_url = f"https://habitica.com/api/v3/tasks/{task_id}"
	result = requests.delete(delete_task_url, headers=auth_headers).json()
	return result["success"] is True

# gets all of the users habitica "todo" tasks
def get_habitica_user_todo_tasks(auth_headers):
	get_tasks_url = "https://habitica.com/api/v3/tasks/user"
	query_params = {"type": "todos"}
	result = requests.get(get_tasks_url, query_params, headers=auth_headers).json()
	if result["success"] is True:
		return result["data"]
	return None

# marks habitica task with task id as done
def complete_habitica_task(auth_headers, task_id):
	complete_task_url = f"https://habitica.com/api/v3/tasks/{task_id}/score/up"
	result = requests.post(complete_task_url, headers=auth_headers).json()
	return result["success"] is True