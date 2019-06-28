import sentry_sdk
import pandas as pd
from chalice import Chalice
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from chalice import BadRequestError
from utils import _files_to_dataframe
from ehba import _calculate_ehba

app = Chalice(app_name='ehba')

# Setup Sentry for error logging for Lambda
sentry_sdk.init(
    dsn="https://5275d10c9ffc4e008a5aec4d4c62052c@sentry.io/1492959",
    integrations=[AwsLambdaIntegration()]
)

@app.route('/status')
def index():
    return {'status': 'ok'}

@app.route('/parse', methods=['POST'])
def parse():
    print(app.current_request.to_dict())
    # TODO: _files_to_dataframe(files)
    results = _calculate_ehba(df)
    return {
        'status': 'ok',
        'results': results
    }

