from . import session
from .. import resources

def describe_domains(role=None):

    client = session.client("opensearch", role)

    instances = []
    response = client.list_domain_names()
    domains = [d['DomainName'] for d in response['DomainNames']]
    response = client.describe_domains(DomainNames=domains)

    for i in response["DomainStatusList"]:
        i["Name"] = i["DomainName"]
        i["Role"] = role
        i["Kind"] = "es"

        i["Ident"] = resources.build_ident(i, role=role)
        instances.append(i)


    return instances
