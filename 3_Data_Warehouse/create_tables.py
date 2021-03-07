import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries
import boto3

def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
            
    KEY=config['IAM_ROLE']['KEY']
    SECRET=config['IAM_ROLE']['SECRET']
    CLUSTER_ID=config['CLUSTER']['DB_CLUSTER_ID']
    
    ec2 = boto3.resource('ec2',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                    )
    
    redshift = boto3.client('redshift',
                  region_name="us-west-2",
                  aws_access_key_id=KEY,
                  aws_secret_access_key=SECRET)
    
    myClusterProps = redshift.describe_clusters(ClusterIdentifier=CLUSTER_ID)['Clusters'][0]
    
    try:
        vpc = ec2.Vpc(id=myClusterProps['VpcId'])
        defaultSg = list(vpc.security_groups.all())[0]
        print(defaultSg)

        defaultSg.authorize_ingress(
           GroupName='redshift_security_group',
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DB_PORT),
            ToPort=int(DB_PORT)
        )
    except Exception as e:
        print(e)

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()