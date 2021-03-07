## OPTIONAL: Question for the reviewer
 
If you have any question about the starter code or your own implementation, please add it in the cell below. 

For example, if you want to know why a piece of code is written the way it is, or its function, or alternative ways of implementing the same functionality, or if you want to get feedback on a specific part of your code or get feedback on things you tried but did not work.

Please keep your questions succinct and clear to help the reviewer answer them satisfactorily. 

> **_Your question_**

## TODO
- All to PEP8
- keys and distkeys in redshift
- 


## Drafts - Remove 

#     KEY=config['IAM_ROLE']['KEY']
#     SECRET=config['IAM_ROLE']['SECRET']
#     CLUSTER_ID=config['CLUSTER']['DB_CLUSTER_ID']
    
#     ec2 = boto3.resource('ec2',
#                        region_name="us-west-2",
#                        aws_access_key_id=KEY,
#                        aws_secret_access_key=SECRET
#                     )
    
#     redshift = boto3.client('redshift',
#                   region_name="us-west-2",
#                   aws_access_key_id=KEY,
#                   aws_secret_access_key=SECRET)
    
#     myClusterProps = redshift.describe_clusters(ClusterIdentifier=CLUSTER_ID)['Clusters'][0]
    
#     try:
#         vpc = ec2.Vpc(id=myClusterProps['VpcId'])
#         defaultSg = list(vpc.security_groups.all())[0]
#         print(defaultSg)

#         defaultSg.authorize_ingress(
#            GroupName='redshift_security_group',
#             CidrIp='0.0.0.0/0',
#             IpProtocol='TCP',
#             FromPort=int(DB_PORT),
#             ToPort=int(DB_PORT)
#         )
#     except Exception as e:
#         print(e)

#     conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
#     cur = conn.cursor()
