# credit https://github.com/festeh/Double-reward

from logging import info
from os import environ
import time

from flask import Flask, jsonify
from habitica_utils import create_habitica_auth_headers, create_habitica_task, complete_habitica_task
from todoist.api import TodoistAPI
from dotenv import load_dotenv
from flask import request
from threading import Thread
# threading package doesn't run threads in parallel, it runs concurrently
import redis

load_dotenv()
app = Flask(__name__)

r = redis.from_url(environ["REDIS_URL"])

priority_lookup = {
	1: '2', 
	2: '1.5',
	3: '1',
	4: '1'
}

@app.route('/todoist_item_completed', methods=['POST'])
def handle_todoist_webhook():
	request_data = request.get_json()
	task_id = request_data["event_data"]["id"]

	if not r.sismember("jobs", task_id):
		t = Thread(target=create_and_complete_task_in_habitica, args=(request_data,))
		t.start()

	return "OK", 200

def create_and_complete_task_in_habitica(request_data):
	task_id = request_data["event_data"]["id"]
	r.sadd("jobs", task_id)
	task_content = request_data["event_data"]["content"]
	info(f"Task received from Todoist: {task_content}")
	print(f"Task received from Todoist: {task_content}")
	auth_headers = create_habitica_auth_headers()
	todo_priority = int(request_data["event_data"]["priority"])
	priority = priority_lookup[todo_priority]
	created_task_id = create_habitica_task(auth_headers, task_content, priority=priority)
	if not created_task_id:
		raise RuntimeError("Unable to create Habitica Task")
	info(f"Created Habitica task: {created_task_id}")
	print(f"Created Habitica task: {created_task_id}")

	time.sleep(30)

	completed = complete_habitica_task(auth_headers, created_task_id)
	if not completed:
		raise RuntimeError(f"Unable to complete Habitica task: {created_task_id}")
	info(f"Completed Habitica task: {created_task_id}")
	print(f"Completed Habitica task: {created_task_id}")

	print(f"Handled Todoist Webhook for Task: {task_id}")
	return 

@app.route('/todoist_projects')
def todoist_projects():
	token = environ["TODOIST_API_TOKEN"]
	api = TodoistAPI(token)
	api.sync()
	projects = api.state["projects"]
	return jsonify(projects)

if __name__ == "__main__":
	app.run()