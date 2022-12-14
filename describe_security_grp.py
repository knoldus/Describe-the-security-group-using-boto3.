# By MuZakkir Saifi
# import logging for get the logs in  execution
import logging
# import the boto3 which will use to interact  with the aws
import boto3
from botocore.exceptions import ClientError
import json

REGION = input("Please enter the your REGION Name: ")

# this is the configration for the logger_for

logger_for = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

grp_client = boto3.client("ec2", region_name=REGION)


def describe_group(tag, tag_values, max_items):

    try:
        pag = grp_client.get_paginator('describe_security_groups')

        response_iterator = pag.paginate(
            Filters=[{
                'Name': f'tag:{tag}',
                'Values': tag_values
            }],
            PaginationConfig={'MaxItems': max_items})

        result = response_iterator.build_full_result()

        grps_list = []

        for page in result['SecurityGroups']:
            grps_list.append(page)

    except ClientError:
        logger_for.exception('Sorry, Security Groups can not be describe.')
        raise
    else:
        return grps_list


if __name__ == '__main__':
    TAG = input("Enter the TAG NAME: ")
    VALUES = []
    # user will enter the number of elements
    number = int(input("Enter number of elements : "))
    for i in range(0, number):
        elements = input("enter you Tag value")
    
        VALUES.append(elements)
    MAXIMUM_ITEMS = int(input("Enter the Value for MAX ITEMS: "))
    groups = describe_group(TAG, VALUES, MAXIMUM_ITEMS)
    logger_for.info('This is your Security Groups details: ')
    for grp in groups:
        logger_for.info(json.dumps(grp, indent=4) + '\n')
        
        
 