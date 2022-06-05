import logging
import boto3
from botocore.exceptions import ClientError
import json
import random
import traceback


AWS_REGION = 'ap-southeast-1'
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

_ssm = boto3.client('ssm')
activity_arns = json.loads(_ssm.get_parameter(
    Name='copilot-saga-pattern-activity-arns')["Parameter"]["Value"])
SFN_ACTIVITY_ARN = activity_arns['logistic-process']


def process():
    # Randomize with high chance it will succeed.
    return True if random.random() > 0.1 else False


if __name__ == '__main__':
    sfn_client = boto3.client('stepfunctions', region_name=AWS_REGION)
    while True:
        response = sfn_client.get_activity_task(
            activityArn=SFN_ACTIVITY_ARN,
            workerName='worker-logistic'
        )
        try:
            if response["taskToken"]:
                input_payload = json.loads(response["input"])
                logger.info("Received input - {}".format(input_payload))
                # process() is just a dummy function to process the transaction
                if process():
                    # Simulate if the process() successfully processed the transaction
                    input_payload["logistic_state"] = "done"
                    input_payload["logistic_result"] = True
                else:
                    # Simulate if the process() failed processing the transaction
                    input_payload["logistic_state"] = "done"
                    input_payload["logistic_result"] = False
                # Send the response back to SFN
                sfn_client.send_task_success(
                    taskToken=response["taskToken"],
                    output=json.dumps(input_payload)
                )
        except Exception as e:
            logger.error(traceback.print_exc())
            sfn_client.send_task_failure(
                taskToken=response["taskToken"], error="Problem on processing", cause="Logistic-Process")
