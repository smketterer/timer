import eel, os, json, urllib, sys
from typing import Dict
import requests
import base64

def load_config():
    try:
        with open(os.path.expanduser("config.json"), 'r') as f:
            json_data = json.load(f)
            return json_data
    except:
        print("Error loading configuration.")

# Load configuration and initialize session
config = load_config()
session = requests.session()

@eel.expose
def authenticate():
    """Authenticate against the api."""
    data = {
        'username': config['user'],
        'password': config['password'],
        'client_name': config['client_name'],
        'client_vendor': config['client_vendor']
    }
    auth_url = '{}/issue-token'.format(config['url'])
    r = session.post(auth_url, data=data)
    try:
        token = r.json()['token']
        # print(token)
        return token
    except:
        return False

token = authenticate()

@eel.expose
def get(url):
    """Make a get call to the API."""
    headers = {'X-Angie-AuthApiToken': token}
    url = '{}{}'.format(config['url'], url)
    r = session.get(url, headers=headers)
    return r.json()

@eel.expose
def post(url, data):
    """Make post call to the API."""
    headers = {'X-Angie-AuthApiToken': token}
    url = '{}{}'.format(config['url'], url)
    r = session.post(url, data=data, headers=headers)
    return r.json()

@eel.expose
def delete(url):
    """Make delete call to the API."""
    headers = {'X-Angie-AuthApiToken': token}
    url = '{}{}'.format(config['url'], url)
    r = session.delete(url, headers=headers)
    return r.json()

@eel.expose
def put(url):
    """Make put call to the API."""
    headers = {'X-Angie-AuthApiToken': token}
    url = '{}{}'.format(config['url'], url)
    r = session.post(url, data=data, headers=headers)
    return r.json()

@eel.expose
def get_url():
    """Get the non-API url."""
    url = config['url'].split("/api/")[0]
    return url

@eel.expose
def get_info():
    """Get info about the system information."""
    message = get('/info')
    return message

@eel.expose
def get_job_types():
    """Get the available job types."""
    message = get('/job-types')
    return message

@eel.expose
def get_projects():
    """Get the projects."""
    message = get('/projects')
    return message

@eel.expose
def get_users():
    """Get the users."""
    message = get('/users')
    return message

@eel.expose
def get_user():
    """Get the current user object."""
    users = get_users()
    user = next(x for x in users if x['email'] == config['user'])
    message = get('/users/{}/'.format(user['id']))
    # print(message)
    return message

@eel.expose
def get_time_records(user_id):
    """Get the time records for a user."""
    message = get('/users/{}/time-records'.format(user_id))
    return message

@eel.expose
def get_tasks():
    """Get all tasks."""
    tasks = []
    for project in get_projects():
        for task in get('/projects/{}/tasks'.format(project['id']))['tasks']:
            tasks.append(task)
    return tasks

@eel.expose
def get_tasks_by_project(project_id):
    """Get the tasks for a specific project."""
    message = get('/projects/{}/tasks'.format(project_id))
    return message

@eel.expose
def complete_task(task_id):
    """Get complete a given task."""
    message = put('/complete/task/{}'.format(task_id))
    return message

@eel.expose
def create_time_record(project_id, task_id, job_type_id, date, time_value, billable, summary):
    users = get_users()
    user = next(x for x in users if x['email'] == config['user'])
    data = {
        'value': time_value,
        'task_id': task_id if task_id else None,
        'user_id': user['id'],
        'job_type_id': job_type_id,
        'record_date': date,
        'billable_status': billable,
        'summary': summary,
    }
    url = '/projects/{}/time-records'.format(project_id)
    return post(url, data)

@eel.expose
def list_daily_time_records(date):
    users = get_users()
    user = next(x for x in users if x['email'] == config['user'])
    r = get_time_records(user['id'])
    time_records = r['time_records']
    time_zone_seconds_offset = 3600 * 6
    # @TODO: This seems to change sometimes, breaking everything.
    # print(date - time_zone_seconds_offset)
    # actual: 1557360000
    # search: 1557356400
    # difference: 3600
    daily_time_records = [x for x in time_records if x['record_date'] == date - time_zone_seconds_offset]
    return daily_time_records

eel.init('web')
eel.start('index.html', size=(400, 600), options={
    'port': 8888
})
