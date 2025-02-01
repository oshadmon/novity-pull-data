from rest_code import execute_get, publish_policy
import json

FROM = '23.239.12.151:32349'
CONN = '104.237.130.228:32049'
policies = execute_get(conn=FROM, command="blockchain get table where dbms=cos")
for policy in policies:
    for key in ['source', 'date', 'ledger']:
        del policy['table'][key]
    output = execute_get(conn=CONN, command=f"blockchain get table where name={policy['table']['name']}")
    if not output:
        publish_policy(conn=CONN, policy=policy)

policies = execute_get(conn=FROM, command='blockchain get cluster where company="Smart City"')
for policy in policies:
    for key in ['date', 'ledger']:
        del policy['cluster'][key]
    if 'parent' not in policy['cluster']:
        output = execute_get(conn=CONN, command=f"blockchain get cluster where id={policy['cluster']['id']}")
        if not output:
            publish_policy(conn=CONN, policy=policy)

for policy in policies:
    output = execute_get(conn=CONN, command=f"blockchain get cluster where id={policy['cluster']['id']}")
    if not output:
        publish_policy(conn=CONN, policy=policy)

policies = execute_get(conn=FROM, command='blockchain get operator where company="Smart City"')
for policy in policies:
    for key in ['date', 'ledger']:
        del policy['operator'][key]
    output = execute_get(conn=CONN, command=f"blockchain get operator where name={policy['operator']['name']}")
    if not output:
        publish_policy(conn=CONN, policy=policy)