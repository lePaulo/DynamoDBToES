import boto3,time,os
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from concurrent.futures import ThreadPoolExecutor

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):

    timeout = time.time() + 60*4
    es = connect_elastic_search(os.getenv('DomainEndpoint'))
    response = {}
    response['hasNext'] = False

    table = dynamodb.Table(event['tablename'])

    if event.get('response'):
        if event['response']['hasNext']:
            tablescan = table.scan(ExclusiveStartKey=event['response']['lastEvaluatedKey'])
    else:
        tablescan = table.scan()

    sortkey = ""
    if event.get('sortkey'):
        sortkey = event['sortkey']
    
    send_to_es(es, tablescan['Items'], event['tablename'], event['partitionkey'], sortkey)

    while 'LastEvaluatedKey' in tablescan:
        tablescan = table.scan(ExclusiveStartKey=tablescan['LastEvaluatedKey'])
        send_to_es(es, tablescan['Items'], event['tablename'], event['partitionkey'], sortkey)
        if time.time() > timeout:
            break
    if tablescan.get('LastEvaluatedKey'):
      response['lastEvaluatedKey'] = tablescan['LastEvaluatedKey']
      response['hasNext'] = True
    return response

def send_to_es(es, items, index_name, partitionkey_name, sortkey_name):
    print('Entering index function for {} items'.format(len(items)))
    def index(item):
        item_sort_key = ""
        if len(sortkey_name) > 0:
            item_sort_key = item[sortkey_name]
        es.index(index=index_name.lower(), doc_type='dynamodb_item', id=item[partitionkey_name]+item_sort_key, body=item)
    with ThreadPoolExecutor() as executor:
      future = executor.map(index,items)
      response = list(future)
    return(response)

def connect_elastic_search(endpoint):
    #connect to the elasticsearch cluster with the domain endpoint from environment variables
    session = boto3.session.Session()
    credentials = session.get_credentials()
    awsauth = AWS4Auth(credentials.access_key,
                       credentials.secret_key,
                       session.region_name, 'es',
                       session_token=credentials.token)
    return Elasticsearch(hosts=[{'host': endpoint, 'port': 443}], http_auth=awsauth,
                         use_ssl=True, verify_certs=True, connection_class=RequestsHttpConnection)