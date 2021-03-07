## How to Run Project
1. Run create_cluster.py
  - it may take a few minutes until the cluster becomes 'available'.
  - run multiple times creat_cluster.py as once the cluster is avaialble, the script
  will return the cluster's endpoint
  - add the endpoint to the config file under CLUSTER/HOST.
2. Run create_tables.py
3. Run etl.py
4. Run clean_up_resources.py to delete the cluster and the role created at step 1.
Run this multiple times until you receive 'Cluster not found' to make sure you deleted it.
