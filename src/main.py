import os

from google.cloud import secretmanager
from googleapiclient.discovery import build


project_id = os.environ.get('GCP_PROJECT')

def get_token():
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(
        {"name": f"projects/{project_id}/secrets/canvas-token/versions/latest"})
    
    return response.payload.data.decode("UTF-8")


def canvas(request):

    environment = {
        'tempLocation': 'gs://canvas-lms-extracts/temp',
        'maxWorkers': '3'
    }

    parameters = {
        'endpoint': request.args.get('endpoint'),
        'start_date': request.args.get('start_date'),
        'base_url': 'https://framinghamk12.instructure.com',
        'token': get_token()
    }

    body = {
        'launchParameter': {
            'jobName': request.args.get('endpoint'),
            'parameters': parameters,
            'environment': environment,
            'containerSpecGcsPath': 'gs://canvas-lms-extracts/dataflow/templates/canvas_etl.json'
        }
    }

    service = build('dataflow', 'v1b3', cache_discovery=False)

    request = service.projects().locations().flexTemplates().launch(
        projectId=project_id,
        location='us-central1',
        body=body
    )
    response = request.execute()
    return response
