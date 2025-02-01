from rest_code import execute_get, publish_policy

FROM = '23.239.12.151:32349'
CONN = '104.237.130.228:32049'
policies = execute_get(conn=FROM, command="blockchain get table where dbms=cos")
for policy in policies:
    output = execute_get(conn=CONN, command=f"blockchain get table where name={policy['table']['name']}")
    if not output:
        publish_policy(conn=CONN, policy=policy)
