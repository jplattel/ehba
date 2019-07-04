import sentry_sdk
import pandas as pd
from chalice import Chalice, Response
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from chalice import BadRequestError
from chalicelib.utils import _files_to_dataframe
from chalicelib.ehba import _calculate_ehba

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
            'X-Content-Type-Options': 'nosniff'
        }
    )

@app.route('/parse', methods=['POST'], cors=True)
def parse():
    print(app.current_request.to_dict())
    # TODO: _files_to_dataframe(files)
    
    df = pd.DataFrame()
    results = _calculate_ehba(df)
    return {
        'status': 'ok',
        'results': results
    }

