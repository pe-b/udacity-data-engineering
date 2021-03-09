import configparser
import boto3


def delete_cluster(redshift, dwh_cluster_identifier):
    """
    Deletes a given cluster.
    Parameters:
    1. redshift client
    2. cluster identifier
    """
    redshift.delete_cluster( ClusterIdentifier=dwh_cluster_identifier,  
                            SkipFinalClusterSnapshot=True)


def detach_policy_and_delete_role(iam, dwh_iam_role_name):
    """
    Detaches policy and deletes the role.
    Parameters:
    1. redshift client
    2. role name associated to cluster
    """
    iam.detach_role_policy(RoleName=dwh_iam_role_name, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
    iam.delete_role(RoleName=dwh_iam_role_name)
    
    
def main():
    
    # Load DW configuration parameters
    config = configparser.ConfigParser()
    config.read_file(open('dwh.cfg'))
    
    KEY                    = config.get('AWS','KEY')
    SECRET                 = config.get('AWS','SECRET')
    
    DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
    DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")
    
    # Create AWS IAM client
    iam = boto3.client('iam',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET)
    
    # Create AWS Redshift client
    redshift = boto3.client('redshift',
                            region_name="us-west-2",
                            aws_access_key_id=KEY,
                            aws_secret_access_key=SECRET)
    
    delete_cluster(redshift, DWH_CLUSTER_IDENTIFIER)
    
    detach_policy_and_delete_role(iam, DWH_IAM_ROLE_NAME)
    
    
if __name__ == "__main__":
    main()

