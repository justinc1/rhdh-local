#!/usr/bin/env python3

import json
import requests
import os
# import requests-oauthlib  # TODO use this

rhdh_url="https://10.44.18.49:7007"
tls_verify=False
token1="eyJ0eXAiOiJ2bmQuYmFja3N0YWdlLnVzZXIiLCJhbGciOiJFUzI1NiIsImtpZCI6ImZjM2Q5NmUzLTY2MDgtNDg0MS1hYTliLTRkMWE4NTkyNTlmNyJ9.eyJpc3MiOiJodHRwczovLzEwLjQ0LjE4LjQ5OjcwMDcvYXBpL2F1dGgiLCJzdWIiOiJ1c2VyOmRlZmF1bHQvYWRtaW4iLCJlbnQiOlsidXNlcjpkZWZhdWx0L2FkbWluIiwiZ3JvdXA6ZGVmYXVsdC90ZWFtLWEtMSIsImdyb3VwOmRlZmF1bHQvdGVhbS1iLTIiXSwiYXVkIjoiYmFja3N0YWdlIiwiaWF0IjoxNzMzNjk4OTg5LCJleHAiOjE3MzM3MDI1ODksInVpcCI6IlRqRHd4aGRER3FfaWlEM2I5aEN3X1FCZ1l1MXd2cWRIdVRBTEE2NmtvenBYOG9fX1FxTUE5dTVTR1ZSZzkzOUlwbkdnaktPZi14d0hqRFlSOVV0NUF3In0.5Q--cAcvs8zON12pC5ccnwD2TnXeP37gJKks6TXVjMHhShTy90sKWFlUft1oxp89SinJe39TN5XDt1VyyVY8yw"
token2="M3Agb3cso6RakaQ1SSkrimVpaeG6dY"
#
aap_url="https://10.44.17.180"
aap_username="admin"
aap_password=os.environ["AAP_PASSWORD"]
# aap_password=""

if tls_verify == False:
    import urllib3
    urllib3.disable_warnings()

def main():
    ss = requests.Session()
    ss.headers.update({
        "Content-Type": "application/json",
        "authorization": f"Bearer {token1}",
    })
    data = json.dumps({
        "token": token2,
        "context": {},
    })

    response = ss.post(rhdh_url + "/api/scaffolder/v2/autocomplete/aap-api-cloud/organizations", data=data, verify=tls_verify)
    objs = response.json()["results"]
    print(f"organizations ({len(objs)}): 0.name={objs[0]['name']}")

    response = ss.post(rhdh_url + "/api/scaffolder/v2/autocomplete/aap-api-cloud/inventories", data=data, verify=tls_verify)
    objs = response.json()["results"]
    print(f"inventories ({len(objs)}): 0.name={objs[0]['name']}")

    task_data = json.dumps({
        "templateRef":"template:default/generic-seed",
        "values":{
            "organization":{
                "id":1,"name":"Default","label":"Default","value":"1"},
                "jobInventory":{"id":1,"name":"Default","label":"Ansible Experience RHEL Inventory","value":"4"},
                "scmUrl":"https://github.com/ansible/ansible-pattern-loader",
                "scmBranch":"main",
                "token":token2,
                "useCases":[
                    {"name":"rhel","url":"https://github.com/justinc1/experience_demo","version":"feature-service-aae"},
                    {"name":"network","url":"https://github.com/rohitthakur2590/network.backup","version":"main"},
                    {"name":"windows","url":"https://github.com/redhat-cop/infra.windows_ops","version":"main"},
                ],
                "playbook":"seed_portal_content.yml",
                "aapUserName":aap_username,
                "aapValidateCerts":False,
                "aapHostName":aap_url,
                "aapPassword":"*******"},
            "secrets":{"aapPassword":aap_password},
    })
    response = ss.post(rhdh_url + "/api/scaffolder/v2/tasks", data=task_data, verify=tls_verify)
    task_id = response.json()["id"]
    print(f"new task : id={task_id}")

    response = ss.get(rhdh_url + f"/api/scaffolder/v2/tasks/{task_id}", verify=tls_verify)
    task = response.json()
    print(f"task : id={task_id} status={task['status']} steps={len(task['spec']['steps'])}")

    response = ss.get(rhdh_url + f"/api/scaffolder/v2/tasks/{task_id}/eventstream", verify=tls_verify, stream=True)
    for event in response:
        print(f"event : {event}")


main()
