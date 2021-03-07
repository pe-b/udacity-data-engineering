import configparser
import boto3
import pandas as pd
import json

        
def create_iam_role_for_redshift(iam, dwh_iam_role_name):
    """
    Creates AWS IAM role for Redshift with S3 read-only permissions.
    Parameters:
    1. Connection to the iam service
    2. Iam role name
    """
    try:
        dwhRole = iam.create_role(
                    Path='/',
                    RoleName=dwh_iam_role_name,
                    Description="Allows Redshift clusters to call AWS services on your behalf.",
                    AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                   'Effect': 'Allow',
                   'Principal': {'Service': 'redshift.amazonaws.com'}}],
                 'Version': '2012-10-17'}))        
    except Exception as e:
        print(e)
    
    iam.attach_role_policy(RoleName=dwh_iam_role_name,
                       PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                      )['ResponseMetadata']['HTTPStatusCode']
                         
        
def get_iam_arn(dwh_iam_role_name):
    """
    Returns the arn for the given role name.
    Parameters:
    1. IAM role name
    """
    return iam.get_role(RoleName=dwh_iam_role_name)['Role']['Arn']
    
    
def create_redshift_cluster(dwh_cluster_type, dwh_node_type, dwh_num_nodes,
                            dwh_db, dwh_cluster_identifier, dwh_db_user,
                            dwh_db_password, roleArn, redshift):
    """
    Creates a redshift cluster.
    Parameters:
    1. Cluster type
    2. Node type
    3. Number of nodes in cluster
    4. Cluster database name
    5. Cluster identifier
    6. Database user
    7. Password for db user
    8. Role arn
    9. Redshift client
    """
    try:
        response = redshift.create_cluster(        
            #Hardware
            ClusterType=dwh_cluster_type,
            NodeType=dwh_node_type,
            NumberOfNodes=int(dwh_num_nodes),

            #Identifiers & Credentials
            DBName=dwh_db,
            ClusterIdentifier=dwh_cluster_identifier,
            MasterUsername=dwh_db_user,
            MasterUserPassword=dwh_db_password,

            #Roles (for s3 access)
            IamRoles=[roleArn])
        
    except Exception as e:
        print(e)
        
        
def open_connection(ec2, myClusterProps, dwh_port):
    """
    Authorises access to redshift cluster.
    Parameters:
    1. EC2 client
    2. Cluster properties
    3. Dwh port
    """
    try:
        vpc = ec2.Vpc(id=myClusterProps['VpcId'])
        defaultSg = list(vpc.security_groups.all())[0]
        print(defaultSg)

        defaultSg.authorize_ingress(
           GroupName=defaultSg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(dwh_port),
            ToPort=int(dwh_port))
    except Exception as e:
        print(e)
        
        
def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

        
def main():
    
    # Load DW configuration parameters
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))

    KEY                    = config.get('AWS','KEY')
    SECRET                 = config.get('AWS','SECRET')

    DWH_CLUSTER_TYPE       = config.get("DWH","DWH_CLUSTER_TYPE")
    DWH_NUM_NODES          = config.get("DWH","DWH_NUM_NODES")
    DWH_NODE_TYPE          = config.get("DWH","DWH_NODE_TYPE")

    DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
    DWH_DB                 = config.get("DWH","DWH_DB")
    DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
    DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
    DWH_PORT               = config.get("DWH","DWH_PORT")
    DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")
    
    # Create AWS clients
    ec2 = boto3.resource('ec2',
                         region_name="us-west-2",
                         aws_access_key_id=KEY,
                         aws_secret_access_key=SECRET)

    s3 = boto3.resource('s3',
                        region_name="us-west-2",
                        aws_access_key_id=KEY,
                        aws_secret_access_key=SECRET)

    iam = boto3.client('iam',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET)

    redshift = boto3.client('redshift',
                            region_name="us-west-2",
                            aws_access_key_id=KEY,
                            aws_secret_access_key=SECRET)
    
    create_iam_role_for_redshift(iam, DWH_IAM_ROLE_NAME)
    
#     roleArn = get_iam_arn(iam, DWH_IAM_ROLE_NAME)
    print('1.3 Get the IAM role ARN')
    roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']

    print(roleArn)
    
    create_redshift_cluster(DWH_CLUSTER_TYPE, DWH_NODE_TYPE,
                            DWH_NUM_NODES, DWH_DB, DWH_CLUSTER_IDENTIFIER,
                            DWH_DB_USER, DWH_DB_PASSWORD, roleArn, redshift)
    
    myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    
    prettyRedshiftProps(myClusterProps)
    
    # Redshift cluster endpoint and ARN role
    DWH_ENDPOINT = myClusterProps['Endpoint']['Address']
    DWH_ROLE_ARN = myClusterProps['IamRoles'][0]['IamRoleArn']
    print("DWH_ENDPOINT :: ", DWH_ENDPOINT)
    print("DWH_ROLE_ARN :: ", DWH_ROLE_ARN)
    
    open_connection(ec2, myClusterProps, DWH_PORT)
    

if __name__ == "__main__":
    main()
