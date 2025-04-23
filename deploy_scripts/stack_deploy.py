import boto3
import logging
from botocore.exceptions import WaiterError, ValidationError

client = boto3.client('cloudformation', region_name="ap-south-1")

logging.getLogger().setLevel("INFO")


class StackCreation:
    def __init__(self, stack_name, reading, parameter):
        self.stack_name = stack_name
        self.reading = reading
        self.parameter = parameter

    def create_stack(self):
        try:
            client.create_stack(
                StackName=self.stack_name,
                TemplateBody=self.reading,
                Capabilities=['CAPABILITY_NAMED_IAM'],
                Parameters=self.parameter
            )
            logging.info("Creating Stack")
            waiter = client.get_waiter('stack_create_complete')
            waiter.wait(
                StackName=self.stack_name,
                WaiterConfig={
                    "Delay": 60,
                    "MaxAttempts": 200
                }
            )
            logging.info("Stack Created")
        except WaiterError:
            pass
        except client.exceptions.AlreadyExistsException:
            logging.info("Updating stack")
            try:
                client.update_stack(
                    StackName=self.stack_name,
                    TemplateBody=self.reading,
                    Capabilities=['CAPABILITY_NAMED_IAM'],
                    Parameters=self.parameter
                )
                waiter = client.get_waiter('stack_update_complete')
                waiter.wait(
                    StackName=self.stack_name,
                    WaiterConfig={
                        "Delay": 60,
                        "MaxAttempts": 200
                    }
                )
            except WaiterError:
                pass
            except client.exceptions.ClientError as err:
                logging.warning(f"{err}")
            logging.info("Stack updated")

    def stack_status(self):
        try:
            response = client.describe_stacks(
                StackName=self.stack_name
            )
            res = response['Stacks'][0]['StackStatus']
            print(res)
            while res == "CREATE_IN_PROGRESS" or res == "ROLLBACK_IN_PROGRESS":
                response = client.describe_stacks(
                    StackName=self.stack_name
                )
                res = response['Stacks'][0]['StackStatus']
        except ValidationError:
            raise Exception("Stack is not present")
        if res == 'ROLLBACK_COMPLETE':
            stack_events = client.describe_stack_events(StackName=self.stack_name)['StackEvents']
            for i in stack_events:
                try:
                    print(i['LogicalResourceId'], end=" ")
                    print(i['ResourceType'], end="  ")
                    print(i['ResourceStatus'], end="  ")
                    print(i['ResourceStatusReason'])
                except KeyError:
                    pass
            client.delete_stack(
                StackName=self.stack_name
            )
            logging.info("Delete Complete")
        else:
            logging.info("Template is created or updated successfully")
            logging.info(f"Api gateway endpoint: {response['Stacks'][0]['Outputs'][0]['OutputValue']}")
