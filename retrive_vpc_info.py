import boto3


ec2_client = boto3.client('ec2', region_name="ap-south-1")

def fetch_vpc_subnets():
    """This function fetches default vpc and subnets"""
    vpc_id = ec2_client.describe_vpcs()["Vpcs"][0]["VpcId"]
    subnet_response = ec2_client.describe_subnets(
        Filters = [{
            'Name': 'vpc-id',
            'Values': [vpc_id]
        }]
    )
    list_subnet = list()
    for subnet_id in subnet_response["Subnets"]:
        list_subnet.append(subnet_id["SubnetId"])
    return [vpc_id, ", ".join(list_subnet)]

if __name__ == "__main__":
    fetch_vpc_subnets()
