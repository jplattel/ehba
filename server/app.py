import sentry_sdk
import pandas as pd
from chalice import Chalice, Response
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from chalice import BadRequestError
from chalicelib.utils import parsed_json_files_to_dataframe
# from chalicelib.ehba import _calculate_ehba

app = Chalice(app_name='ehba')

# Setup Sentry for error logging for Lambda
sentry_sdk.init(
    dsn="https://5275d10c9ffc4e008a5aec4d4c62052c@sentry.io/1492959",
    integrations=[AwsLambdaIntegration()]
)

@app.route('/status', cors=True)
def index():
    return Response(
        body={'status': 'ok'},
        status_code=200,
        headers={
            'Content-Type': 'text/json',
        }
    )

@app.route('/parse', methods=['POST'], cors=True)
def parse():
    parsed_json_files = app.current_request.json_body.get("files", [])

    data, results = parsed_json_files_to_dataframe(parsed_json_files)
    # data.replace({pd.np.nan: None})
    data.reset_index(drop=True)
    return Response(
        body={
            'status': 'ok',
            'counts': {
                'files': len(parsed_json_files)
            },
            'charts': {},
            'data': data.to_dict(orient='index'),
            'results': results
        },
        status_code=200,
        headers={
            'Content-Type': 'text/json',
        }
    )