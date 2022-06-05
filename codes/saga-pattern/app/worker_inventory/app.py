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
SFN_ACTIVITY_ARN = activity_arns['inventory-process']


'''
This is an enhanced process that is reserved for next iteration
'''


def force_process(force_process=False):
    # Check if we have to force the process to succeed or fail based on the force_process. This is used only for testing
    if force_process is not None:
        return force_process
    else:
        # Randomize with high chance it will succeed.
        return True if random.random() > 0.1 else False


'''
EOF
'''


def process(force_process=False):
    # Randomize with high chance it will succeed.
    return True if random.random() > 0.1 else False


if __name__ == '__main__':
    sfn_client = boto3.client('stepfunctions', region_name=AWS_REGION)
    while True:
        response = sfn_client.get_activity_task(
            activityArn=SFN_ACTIVITY_ARN,
            workerName='worker-inventory'
        )
        try:
            print(response)
            if response["taskToken"]:
                input_payload = json.loads(response["input"])
                # if input_payload["inventory_state"] == "process":
                logger.info("Received input - {}".format(input_payload))
                # process() is just a dummy function to process the transaction
                if process():
                    # Simulate if the process() successfully processed the transaction
                    input_payload["inventory_state"] = "done"
                    input_payload["inventory_result"] = True
                else:
                    # Simulate if the process() failed processing the transaction
                    input_payload["inventory_state"] = "done"
                    input_payload["inventory_result"] = False

                # Send the response back to SFN
                sfn_client.send_task_success(
                    taskToken=response["taskToken"],
                    output=json.dumps(input_payload)
                )
        except Exception as e:
            logger.error(traceback.print_exc())
            sfn_client.send_task_failure(
                taskToken=response["taskToken"], error="Problem on processing", cause="Inventory-Process")
