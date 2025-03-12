
import json

import boto3


def process(service, request):
    args = {'site': service, 'lookup': request}
    print(args)
    client = boto3.client('lambda', region_name='us-east-2')
    response = client.invoke(
        FunctionName='arn:aws:lambda:us-east-2:332807454899:function:lambda-html',
        InvocationType='RequestResponse',
        LogType='None',
        Payload=json.dumps(args)
    )
    if service == "dotabuff":
        data = response['Payload'].read().decode('unicode_escape')
    else:
        data = response['Payload'].read().decode()
    return data
