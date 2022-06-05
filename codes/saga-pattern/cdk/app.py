#!/usr/bin/env python3
from constructs import Construct
from aws_cdk import App, Stack
from aws_cdk import aws_stepfunctions as _sfn
from aws_cdk import aws_stepfunctions_tasks as _sfn_tasks
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_ssm as _ssm
import aws_cdk as core
import json


class CdkStack(Stack):
    def __init__(self, scope: Construct, id: str, stack_prefix: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        inventory_process = _sfn.Activity(self, "Inventory-Process")
        inventory_rollback = _sfn.Activity(self, "Inventory-Rollback")
        payment_process = _sfn.Activity(self, "Payment-Process")
        payment_rollback = _sfn.Activity(self, "Payment-Rollback")
        logistic_process = _sfn.Activity(self, "Logistic-Process")
        logistic_rollback = _sfn.Activity(self, "Logistic-Rollback")

        activity_inventory_process = _sfn_tasks.StepFunctionsInvokeActivity(self, "Inventory Process",
                                                                            activity=inventory_process
                                                                            )
        activity_inventory_rollback = _sfn_tasks.StepFunctionsInvokeActivity(self, "Cancel Inventory",
                                                                             activity=inventory_rollback
                                                                             )
        activity_payment_process = _sfn_tasks.StepFunctionsInvokeActivity(self, "Payment Process",
                                                                          activity=payment_process
                                                                          )
        activity_payment_rollback = _sfn_tasks.StepFunctionsInvokeActivity(self, "Cancel Payment",
                                                                           activity=payment_rollback
                                                                           )
        activity_logistic_process = _sfn_tasks.StepFunctionsInvokeActivity(self, "Logistic Process",
                                                                           activity=logistic_process
                                                                           )
        activity_logistic_rollback = _sfn_tasks.StepFunctionsInvokeActivity(self, "Cancel Logistic",
                                                                            activity=logistic_rollback
                                                                            )

        state_succeed = _sfn.Succeed(self, "Transaction success")
        state_failed = _sfn.Fail(self, "Transaction failed")

        c_inventory_check = _sfn.Choice(self, "Inventory check ok?")
        c_inventory_check.when(_sfn.Condition.boolean_equals(
            "$.inventory_result", True), activity_payment_process)
        c_inventory_check.when(_sfn.Condition.boolean_equals(
            "$.inventory_result", False), activity_inventory_rollback)

        activity_inventory_rollback.next(state_failed)

        c_payment_check = _sfn.Choice(self, "Payment check ok?")
        c_payment_check.when(_sfn.Condition.boolean_equals(
            "$.payment_result", True), activity_logistic_process)
        c_payment_check.when(_sfn.Condition.boolean_equals(
            "$.payment_result", False), activity_payment_rollback)

        activity_payment_process.next(c_payment_check)
        activity_payment_rollback.next(activity_inventory_rollback)

        c_logistic_check = _sfn.Choice(self, "Logistic check ok?")
        c_logistic_check.when(_sfn.Condition.boolean_equals(
            "$.logistic_result", True), state_succeed)
        c_logistic_check.when(_sfn.Condition.boolean_equals(
            "$.logistic_result", False), activity_logistic_rollback)

        activity_logistic_process.next(c_logistic_check)
        activity_logistic_rollback.next(activity_payment_rollback)

        definition = activity_inventory_process.next(c_inventory_check)
        _sfn.StateMachine(
            self,
            "copilot-saga-pattern",
            definition=definition,
            timeout=core.Duration.minutes(5))

        # Use this dict into SSM for easy access by Workers.
        activity_arns = {
            "inventory-process": inventory_process.activity_arn,
            "inventory-rollback": inventory_rollback.activity_arn,
            "payment-process": payment_process.activity_arn,
            "payment-rollback": payment_rollback.activity_arn,
            "logistic-process": logistic_process.activity_arn,
            "logistic-rollback": logistic_rollback.activity_arn,
        }

        ssm_activity_arns = _ssm.StringParameter(self, "{}-activity-arns".format(stack_prefix),
                                                 description='List of activity ARNs for Workers',
                                                 parameter_name="{}-activity-arns".format(
            stack_prefix),
            string_value=json.dumps(activity_arns)
        )

        # This part is a bit complicated.
        task_roles = self.node.try_get_context("list_ecs_task_roles")
        for key in task_roles:
            iam_for_worker = _iam.Role.from_role_arn(self, "{}-worker-taskrole-{}".format(
                stack_prefix, key), role_arn="arn:aws:iam::{}:role/{}".format(core.Aws.ACCOUNT_ID, task_roles[key]))

            sfn_policy_statement = _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW)
            sfn_policy_statement.add_actions("states:GetActivityTask")
            sfn_policy_statement.add_actions("states:SendTaskSuccess")
            sfn_policy_statement.add_actions("states:SendTaskFailure")
            sfn_policy_statement.add_actions("states:DescribeActivity")
            sfn_policy_statement.add_actions("states:SendTaskHeartbeat")

            if key == "worker_inventory":
                sfn_policy_statement.add_resources(
                    inventory_process.activity_arn)
            elif key == "worker_inventory_rollback":
                sfn_policy_statement.add_resources(
                    inventory_rollback.activity_arn)
            elif key == "worker_payment":
                sfn_policy_statement.add_resources(
                    payment_process.activity_arn)
            elif key == "worker_payment_rollback":
                sfn_policy_statement.add_resources(
                    payment_rollback.activity_arn)
            elif key == "worker_logistic":
                sfn_policy_statement.add_resources(
                    logistic_process.activity_arn)
            elif key == "worker_logistic_rollback":
                sfn_policy_statement.add_resources(
                    logistic_rollback.activity_arn)
            iam_for_worker.add_to_principal_policy(sfn_policy_statement)
            ssm_activity_arns.grant_read(iam_for_worker)

        core.CfnOutput(self,
                       "{}-activity-inventory-process".format(stack_prefix),
                       value=inventory_process.activity_arn,
                       export_name="{}-activity-inventory-process".format(stack_prefix))
        core.CfnOutput(self,
                       "{}-activity-inventory-rollback".format(stack_prefix),
                       value=inventory_rollback.activity_arn,
                       export_name="{}-activity-inventory-rollback".format(stack_prefix))
        core.CfnOutput(self,
                       "{}-activity-payment-process".format(stack_prefix),
                       value=payment_process.activity_arn,
                       export_name="{}-activity-payment-process".format(stack_prefix))
        core.CfnOutput(self,
                       "{}-activity-payment-rollback".format(stack_prefix),
                       value=payment_rollback.activity_arn,
                       export_name="{}-activity-payment-rollback".format(stack_prefix))
        core.CfnOutput(self,
                       "{}-activity-logistic-process".format(stack_prefix),
                       value=logistic_process.activity_arn,
                       export_name="{}-activity-logistic-process".format(stack_prefix))
        core.CfnOutput(self,
                       "{}-activity-logistic-rollback".format(stack_prefix),
                       value=logistic_rollback.activity_arn,
                       export_name="{}-activity-logistic-rollback".format(stack_prefix))
        core.CfnOutput(self,
                       "{}-ssm-activity-arns".format(stack_prefix),
                       value=ssm_activity_arns.parameter_arn,
                       export_name="{}-ssm-activity-arns".format(stack_prefix))
        core.CfnOutput(self,
                       "{}-ssm-activity-name".format(stack_prefix),
                       value=ssm_activity_arns.parameter_name,
                       export_name="{}-ssm-activity-name".format(stack_prefix))


stack_prefix = 'copilot-saga-pattern'
app = core.App()
stack = CdkStack(app, stack_prefix, stack_prefix=stack_prefix)
core.Tags.of(stack).add('Name', stack_prefix)

app.synth()
