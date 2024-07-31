import logging
import boto3
import random
import time
import zipfile
from io import BytesIO
import json
import uuid
import pprint
import os
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from fetch_aws_best_practices import *

### NOTE: change the logging level to DEBUG if infrasetup fails to get more trace on the issue
logging.basicConfig(format='[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

prefix_infra = None
prefix_iam = None
suffix = None

sts_client = boto3.client('sts')
iam_client = boto3.client('iam')
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

session = boto3.session.Session()
region = session.region_name
account_id = sts_client.get_caller_identity()["Account"]
region, account_id
# getting boto3 clients for required AWS services

from botocore.config import Config 

timeout_config = Config(read_timeout=1800)

bedrock_agent_client = boto3.client('bedrock-agent')
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime', config=timeout_config)
open_search_serverless_client = boto3.client('opensearchserverless')

# getting boto3 clients for required AWS services
sts_client = boto3.client('sts')
iam_client = boto3.client('iam')
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')



def generate_prefix_for_agent_infra():
    random_uuid = str(uuid.uuid4())
    prefix_infra = 'l2' + random_uuid[0:6]
    prefix_iam = 'l2'+ random_uuid.split('-')[1]
    
    logger.info(f"random_uuid :: {random_uuid} prefix_infra :: {prefix_infra} prefix_iam :: {prefix_iam}")
    return prefix_infra, prefix_iam


def setup_agent_infrastructure():
    
    # prefix and suffix names
    prefix_infra, prefix_iam = generate_prefix_for_agent_infra()
    suffix = f"{account_id}" #{region}-

    agent_name = f"{prefix_infra}-agent-kb"
    agent_alias_name = f"{prefix_infra}-workshop-alias"
    bucket_name = f'{agent_name}-{suffix}'
    bucket_arn = f"arn:aws:s3:::{bucket_name}"
    schema_key = f'{agent_name}-schema.json' # file in repo
    schema_name = 'appbuilder_agent_openapi_schema_with_kb.json'
    schema_arn = f'arn:aws:s3:::{bucket_name}/{schema_key}'
    bedrock_agent_bedrock_allow_policy_name = f"{prefix_iam}-bedrock-allow-{suffix}"
    bedrock_agent_s3_allow_policy_name = f"{prefix_iam}-s3-allow-{suffix}"
    bedrock_agent_kb_allow_policy_name = f"{prefix_iam}-kb-allow-{suffix}"
    lambda_role_name = f'{agent_name}-lambda-role-{suffix}'
    agent_role_name = f'AmazonBedrockExecutionRoleForAgents_{prefix_iam}'
    lambda_code_path = f"lambda_function_appbuilder.py" # file in repo
    lambda_name = f'{agent_name}-{suffix}'

    ## KB with DB
    kb_db_tag = 'kbdb'

    kb_db_name = f'{prefix_infra}-{kb_db_tag}-{suffix}'
    kb_db_data_source_name = f'{prefix_infra}-{kb_db_tag}-docs-{suffix}'
    kb_db_files_path = f'kb_appbuilder/northwind_db' # file path keep as-is
    kb_db_key = f'{kb_db_tag}_{prefix_infra}'
    kb_db_role_name = f'AmazonBedrockExecutionRoleForKnowledgeBase_{prefix_infra}_{kb_db_tag}_icakb'
    kb_db_bedrock_allow_policy_name = f"ica-{kb_db_tag}-{prefix_infra}-bedrock-allow-{suffix}"
    kb_db_aoss_allow_policy_name = f"ica-{kb_db_tag}-{prefix_infra}-aoss-allow-{suffix}"
    kb_db_s3_allow_policy_name = f"ica-{kb_db_tag}-{prefix_infra}-s3-allow-{suffix}"
    kb_db_collection_name = f'{prefix_iam}-{kb_db_tag}-{suffix}' 
    # Select Amazon titan as the embedding model
    kb_db_embedding_model_arn = f'arn:aws:bedrock:{region}::foundation-model/amazon.titan-embed-text-v1'
    kb_db_vector_index_name = f"bedrock-knowledge-base-{prefix_infra}-{kb_db_tag}-index"
    kb_db_metadataField = f'bedrock-knowledge-base-{prefix_infra}-{kb_db_tag}-metadata'
    kb_db_textField = f'bedrock-knowledge-base-{prefix_infra}-{kb_db_tag}-text'
    kb_db_vectorField = f'bedrock-knowledge-base-{prefix_infra}-{kb_db_tag}-vector'

    ## KB with AWS
    kb_aws_tag = 'kbaws'

    kb_aws_name = f'{prefix_infra}-{kb_aws_tag}-{suffix}'
    kb_aws_data_source_name = f'{prefix_infra}-{kb_aws_tag}-docs-{suffix}'
    kb_aws_files_path = f'kb_appbuilder/aws_best_practices_2' # file path keep as-is
    kb_aws_key = f'{kb_aws_tag}_{prefix_infra}'
    kb_aws_role_name = f'AmazonBedrockExecutionRoleForKnowledgeBase_{prefix_infra}_{kb_aws_tag}_icakb'
    kb_aws_bedrock_allow_policy_name = f"ica-{kb_aws_tag}-{prefix_infra}-bedrock-allow-{suffix}"
    kb_aws_aoss_allow_policy_name = f"ica-{kb_aws_tag}-{prefix_infra}-aoss-allow-{suffix}"
    kb_aws_s3_allow_policy_name = f"ica-{kb_aws_tag}-{prefix_infra}-s3-allow-{suffix}"
    kb_aws_collection_name = f'{prefix_iam}-{kb_aws_tag}-{suffix}' 
    # Select Amazon titan as the embedding model
    kb_aws_embedding_model_arn = f'arn:aws:bedrock:{region}::foundation-model/amazon.titan-embed-text-v1'
    kb_aws_vector_index_name = f"bedrock-knowledge-base-{prefix_infra}-{kb_aws_tag}-index"
    kb_aws_metadataField = f'bedrock-knowledge-base-{prefix_infra}-{kb_aws_tag}-metadata'
    kb_aws_textField = f'bedrock-knowledge-base-{prefix_infra}-{kb_aws_tag}-text'
    kb_aws_vectorField = f'bedrock-knowledge-base-{prefix_infra}-{kb_aws_tag}-vector'

    agent_name = f"{prefix_infra}-agent-kb"
    agent_alias_name = f"{prefix_infra}-workshop-alias"
    bucket_name = f'{agent_name}-{suffix}'
    bucket_arn = f"arn:aws:s3:::{bucket_name}"
    schema_key = f'{agent_name}-schema.json' # file in repo
    schema_name = 'appbuilder_agent_openapi_schema_with_kb.json'
    schema_arn = f'arn:aws:s3:::{bucket_name}/{schema_key}'
    bedrock_agent_bedrock_allow_policy_name = f"{prefix_iam}-bedrock-allow-{suffix}"
    bedrock_agent_s3_allow_policy_name = f"{prefix_iam}-s3-allow-{suffix}"
    bedrock_agent_kb_allow_policy_name = f"{prefix_iam}-kb-allow-{suffix}"
    lambda_role_name = f'{agent_name}-lambda-role-{suffix}'
    agent_role_name = f'AmazonBedrockExecutionRoleForAgents_{prefix_iam}'
    lambda_code_path = f"lambda_function_appbuilder.py" # file in repo
    lambda_name = f'{agent_name}-{suffix}'


    # ## Knowledge Base 1 : DB

    # ### Create S3 bucket and upload API Schema and Knowledge Base files
    # 
    # Agents require an API Schema stored on s3. Let's create an S3 bucket to store the file and upload the necessary files to the newly created bucket


    # Create S3 bucket for Open API schema
    s3bucket = s3_client.create_bucket(
        Bucket=bucket_name
    )


    # Upload Open API schema to this s3 bucket
    s3_client.upload_file(schema_name, bucket_name, schema_key)

            
    # Upload Knowledge Base files to this s3 bucket
    # the DDL script is required for the LLM to learn how to write queries
    # the .db file is used by lambda to execute queries, it is NOT used in Knowledge base creation
    for f in os.listdir(kb_db_files_path):
        if f.endswith(".sql"):
            s3_client.upload_file(kb_db_files_path+'/'+f, bucket_name, kb_db_key+'/'+f)
            
    for f in os.listdir(kb_db_files_path):
        if f.endswith(".db"):
            s3_client.upload_file(kb_db_files_path+'/'+f, bucket_name, f)



    # ## Knowledge Base 2: AWS


    # Upload Knowledge Base files to this s3 bucket
    # the JSON files for LLM to decide which AWS design best practices to elaborate on
    for f in os.listdir(kb_aws_files_path):
        if f.endswith(".json") or f.endswith(".txt"):
            s3_client.upload_file(kb_aws_files_path+'/'+f, bucket_name, kb_aws_key+'/'+f)


    # ### <a name="4">Create Lambda function for Action Group</a>
    # (<a href="#0">Go to top</a>)
    # 
    # Let's now create the lambda function required by the agent action group. We first need to create the lambda IAM role and it's policy. After that, we package the lambda function into a ZIP format to create the function


    # Create IAM Role for the Lambda function
    try:
        assume_role_policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "bedrock:InvokeModel",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        assume_role_policy_document_json = json.dumps(assume_role_policy_document)

        lambda_iam_role = iam_client.create_role(
            RoleName=lambda_role_name,
            AssumeRolePolicyDocument=assume_role_policy_document_json
        )

        # Pause to make sure role is created
        time.sleep(20)
    except:
        lambda_iam_role = iam_client.get_role(RoleName=lambda_role_name)

    iam_client.attach_role_policy(
        RoleName=lambda_role_name,
        PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    )
    iam_client.attach_role_policy(
        RoleName=lambda_role_name,
        PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
    )


    # Package up the lambda function code
    s = BytesIO()
    z = zipfile.ZipFile(s, 'w')
    z.write(lambda_code_path)
    z.close()
    zip_content = s.getvalue()

    # Create Lambda Function
    lambda_function = lambda_client.create_function(
        FunctionName=lambda_name,
        Runtime='python3.12',
        Timeout=900,
        Role=lambda_iam_role['Role']['Arn'],
        Code={'ZipFile': zip_content},
        Handler='lambda_function_appbuilder.lambda_handler',
        Environment={
            'Variables': {
                'BUCKET_NAME': bucket_name,
                'KB_PREFIX': kb_db_key
            }
        },
    )


    # ### <a name="5">Create Knowledge Base 1 for SQL generation with Northwind Database </a>
    # (<a href="#0">Go to top</a>)
    # 
    # We will now create the knowledge base used by the agent to gather the outstanding documents requirements. We will use [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/) as the vector databse and index the files stored on the previously created S3 bucket

    # #### Create Knowledge Base Role
    # Let's first create IAM policies to allow our Knowledge Base to access Bedrock Titan Embedding Foundation model, Amazon OpenSearch Serverless and the S3 bucket with the Knowledge Base Files.
    # 
    # Once the policies are ready, we will create the Knowledge Base role

    # Create IAM policies for KB to invoke embedding model
    bedrock_kb_db_allow_fm_model_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AmazonBedrockAgentBedrockFoundationModelPolicy",
                "Effect": "Allow",
                "Action": "bedrock:InvokeModel",
                "Resource": [
                    kb_db_embedding_model_arn
                ]
            }
        ]
    }

    kb_db_bedrock_policy_json = json.dumps(bedrock_kb_db_allow_fm_model_policy_statement)

    kb_db_bedrock_policy = iam_client.create_policy(
        PolicyName=kb_db_bedrock_allow_policy_name,
        PolicyDocument=kb_db_bedrock_policy_json
    )


    # Create IAM policies for KB to access OpenSearch Serverless
    bedrock_kb_db_allow_aoss_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "aoss:APIAccessAll",
                "Resource": [
                    f"arn:aws:aoss:{region}:{account_id}:collection/*"
                ]
            }
        ]
    }


    kb_db_aoss_policy_json = json.dumps(bedrock_kb_db_allow_aoss_policy_statement)

    kb_db_aoss_policy = iam_client.create_policy(
        PolicyName=kb_db_aoss_allow_policy_name,
        PolicyDocument=kb_db_aoss_policy_json
    )


    kb_db_s3_allow_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowKBAccessDocuments",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}/*",
                    f"arn:aws:s3:::{bucket_name}"
                ],
                "Condition": {
                    "StringEquals": {
                        "aws:ResourceAccount": f"{account_id}"
                    }
                }
            }
        ]
    }


    kb_db_s3_json = json.dumps(kb_db_s3_allow_policy_statement)
    kb_db_s3_policy = iam_client.create_policy(
        PolicyName=kb_db_s3_allow_policy_name,
        PolicyDocument=kb_db_s3_json
    )
    

    # Create IAM Role for the agent and attach IAM policies
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [{
              "Effect": "Allow",
              "Principal": {
                "Service": "bedrock.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
        }]
    }

    assume_role_policy_document_json = json.dumps(assume_role_policy_document)
    kb_db_role = iam_client.create_role(
        RoleName=kb_db_role_name,
        AssumeRolePolicyDocument=assume_role_policy_document_json
    )

    # Pause to make sure role is created
    time.sleep(20)

    iam_client.attach_role_policy(
        RoleName=kb_db_role_name,
        PolicyArn=kb_db_bedrock_policy['Policy']['Arn']
    )

    iam_client.attach_role_policy(
        RoleName=kb_db_role_name,
        PolicyArn=kb_db_aoss_policy['Policy']['Arn']
    )

    iam_client.attach_role_policy(
        RoleName=kb_db_role_name,
        PolicyArn=kb_db_s3_policy['Policy']['Arn']
    )

    kb_db_role_arn = kb_db_role["Role"]["Arn"]
    logger.debug(f"kb_db_role_arn :: {kb_db_role_arn} ")


    # #### Create Vector Data Base
    # 
    # First of all we have to create a vector store. In this section we will use *Amazon OpenSerach serverless.*
    # 
    # Amazon OpenSearch Serverless is a serverless option in Amazon OpenSearch Service (AOSS). As a developer, you can use OpenSearch Serverless to run petabyte-scale workloads without configuring, managing, and scaling OpenSearch clusters. You get the same interactive millisecond response times as OpenSearch Service with the simplicity of a serverless environment. Pay only for what you use by automatically scaling resources to provide the right amount of capacity for your application—without impacting data ingestion.

    

    # Create OpenSearch Collection
    security_policy_json = {
        "Rules": [
            {
                "ResourceType": "collection",
                "Resource":[
                    f"collection/{kb_db_collection_name}"
                ]
            }
        ],
        "AWSOwnedKey": True
    }
    security_policy = open_search_serverless_client.create_security_policy(
        description='security policy of aoss collection',
        name=kb_db_collection_name,
        policy=json.dumps(security_policy_json),
        type='encryption'
    )
    

    kb_db_network_policy_json = [
      {
        "Rules": [
          {
            "Resource": [
              f"collection/{kb_db_collection_name}"
            ],
            "ResourceType": "dashboard"
          },
          {
            "Resource": [
              f"collection/{kb_db_collection_name}"
            ],
            "ResourceType": "collection"
          }
        ],
        "AllowFromPublic": True
      }
    ]

    kb_db_network_policy = open_search_serverless_client.create_security_policy(
        description='network policy of aoss collection',
        name=kb_db_collection_name,
        policy=json.dumps(kb_db_network_policy_json),
        type='network'
    )

    response = sts_client.get_caller_identity()
    current_role = response['Arn']
    logger.debug(f"current_role :: {current_role} ")
    

    kb_db_data_policy_json = [
      {
        "Rules": [
          {
            "Resource": [
              f"collection/{kb_db_collection_name}"
            ],
            "Permission": [
              "aoss:DescribeCollectionItems",
              "aoss:CreateCollectionItems",
              "aoss:UpdateCollectionItems",
              "aoss:DeleteCollectionItems"
            ],
            "ResourceType": "collection"
          },
          {
            "Resource": [
              f"index/{kb_db_collection_name}/*"
            ],
            "Permission": [
                "aoss:CreateIndex",
                "aoss:DeleteIndex",
                "aoss:UpdateIndex",
                "aoss:DescribeIndex",
                "aoss:ReadDocument",
                "aoss:WriteDocument"
            ],
            "ResourceType": "index"
          }
        ],
        "Principal": [
            kb_db_role_arn,
            f"arn:aws:sts::{account_id}:assumed-role/Admin/*",
            current_role
        ],
        "Description": ""
      }
    ]

    kb_db_data_policy = open_search_serverless_client.create_access_policy(
        description='data access policy for aoss collection',
        name=kb_db_collection_name,
        policy=json.dumps(kb_db_data_policy_json),
        type='data'
    )


    kb_db_opensearch_collection_response = open_search_serverless_client.create_collection(
        description='OpenSearch collection for Amazon Bedrock Knowledge Base for Northwind DB',
        name=kb_db_collection_name,
        standbyReplicas='DISABLED',
        type='VECTORSEARCH'
    )
    
    logger.debug(f"kb_db_opensearch_collection_response :: {kb_db_opensearch_collection_response} ")
    


    kb_db_collection_arn = kb_db_opensearch_collection_response["createCollectionDetail"]["arn"]
    logger.debug(f"kb_db_collection_arn :: {kb_db_collection_arn} ")
    

    # wait for collection creation
    response = open_search_serverless_client.batch_get_collection(names=[kb_db_collection_name])
    # Periodically check collection status
    while (response['collectionDetails'][0]['status']) == 'CREATING':
        print('Creating collection...')
        time.sleep(30)
        response = open_search_serverless_client.batch_get_collection(names=[kb_db_collection_name])
    print('\nCollection successfully created:')
    #print(response["collectionDetails"])
    # Extract the collection endpoint from the response
    host = (response['collectionDetails'][0]['collectionEndpoint'])
    final_host = host.replace("https://", "")
    logger.debug(f"final_host :: {final_host} ")
    


    # #### Create OpenSearch Index
    # 
    # Let's now create a vector index to index our data

    

    credentials = boto3.Session().get_credentials()
    service = 'aoss'
    awsauth = AWS4Auth(
        credentials.access_key, 
        credentials.secret_key,
        region, 
        service, 
        session_token=credentials.token
    )

    # Build the OpenSearch client
    open_search_client = OpenSearch(
        hosts=[{'host': final_host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=300
    )
    # It can take up to a minute for data access rules to be enforced
    time.sleep(45)
    index_body = {
        "settings": {
            "index.knn": True,
            "number_of_shards": 1,
            "knn.algo_param.ef_search": 512,
            "number_of_replicas": 0,
        },
        "mappings": {
            "properties": {}
        }
    }

    index_body["mappings"]["properties"][kb_db_vectorField] = {
        "type": "knn_vector",
        "dimension": 1536,
        "method": {
            "name": "hnsw",
            "engine": "faiss",
            "space_type": "innerproduct",
            "parameters": {
                "ef_construction": 512, 
                "m": 16
            },
        },
    }

    index_body["mappings"]["properties"][kb_db_textField] = {
        "type": "text"
    }

    index_body["mappings"]["properties"][kb_db_metadataField] = {
        "type": "text"
    }

    # Create index
    response = open_search_client.indices.create(kb_db_vector_index_name, body=index_body)
    print('\nCreating index:')
    logger.debug(f"response :: {response} ")


    kb_db_storage_configuration = {
        'opensearchServerlessConfiguration': {
            'collectionArn': kb_db_collection_arn, 
            'fieldMapping': {
                'metadataField': kb_db_metadataField,
                'textField': kb_db_textField,
                'vectorField': kb_db_vectorField
            },
            'vectorIndexName': kb_db_vector_index_name
        },
        'type': 'OPENSEARCH_SERVERLESS'
    }


    # Creating the knowledge base
    try:
        # ensure the index is created and available
        time.sleep(45)
        kb_db_obj = bedrock_agent_client.create_knowledge_base(
            name=kb_db_name, 
            description='KB that contains information to provide accurate responses based on the Northwind database',
            roleArn=kb_db_role_arn,
            knowledgeBaseConfiguration={
                'type': 'VECTOR',  # Corrected type
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': kb_db_embedding_model_arn
                }
            },
            storageConfiguration=kb_db_storage_configuration
        )

        # Pretty print the response
        #pprint.pprint(kb_db_obj)

    except Exception as e:
        print(f"Error occurred: {e}")


    # #### Create a data source that you can attach to the recently created Knowledge Base
    # 
    # Let's create a data source for our Knowledge Base. Then we will ingest our data and convert it into embeddings.

    # Define the S3 configuration for your data source
    s3_configuration = {
        'bucketArn': bucket_arn,
        'inclusionPrefixes': [kb_db_key]  
    }

    # Define the data source configuration
    kb_db_data_source_configuration = {
        's3Configuration': s3_configuration,
        'type': 'S3'
    }

    knowledge_base_db_id = kb_db_obj["knowledgeBase"]["knowledgeBaseId"]
    knowledge_base_db_arn = kb_db_obj["knowledgeBase"]["knowledgeBaseArn"]


    kb_db_chunking_strategy_configuration = {
        "chunkingStrategy": "FIXED_SIZE",
        "fixedSizeChunkingConfiguration": {
            "maxTokens": 1024,
            "overlapPercentage": 50
        }
    }


    # Create the data source
    try:
        # ensure that the KB is created and available
        time.sleep(45)
        kb_db_data_source_response = bedrock_agent_client.create_data_source(
            knowledgeBaseId=knowledge_base_db_id,
            name=kb_db_data_source_name,
            description='DataSource for the Northwind DDL statements',
            dataSourceConfiguration=kb_db_data_source_configuration,
            vectorIngestionConfiguration = {
                "chunkingConfiguration": kb_db_chunking_strategy_configuration
            }
        )

        # Pretty print the response
        #pprint.pprint(kb_db_data_source_response)

    except Exception as e:
        print(f"Error occurred: {e}")


    # #### Start ingestion job
    # Once the Knowledge Base and Data Source are created, we can start the ingestion job.
    # During the ingestion job, Knowledge Base will fetch the documents in the data source, pre-process it to extract text, chunk it based on the chunking size provided, create embeddings of each chunk and then write it to the vector database, in this case Amazon OpenSource Serverless.


    # Start an ingestion job
    kb_db_data_source_id = kb_db_data_source_response["dataSource"]["dataSourceId"]
    start_job_response = bedrock_agent_client.start_ingestion_job(
        knowledgeBaseId=knowledge_base_db_id, 
        dataSourceId=kb_db_data_source_id
    )


    # ### <a name="6">Create Knowledge Base 2 for AWS well-arch </a>
    # (<a href="#0">Go to top</a>)
    # 
    # 
    # We will now create the knowledge base used by the agent to gather the outstanding documents requirements. We will use [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/) as the vector databse and index the files stored on the previously created S3 bucket

    # #### Create Knowledge Base Role
    # Let's first create IAM policies to allow our Knowledge Base to access Bedrock Titan Embedding Foundation model, Amazon OpenSearch Serverless and the S3 bucket with the Knowledge Base Files.
    # 
    # Once the policies are ready, we will create the Knowledge Base role


    # Create IAM policies for KB to invoke embedding model
    bedrock_kb_aws_allow_fm_model_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AmazonBedrockAgentBedrockFoundationModelPolicy",
                "Effect": "Allow",
                "Action": "bedrock:InvokeModel",
                "Resource": [
                    kb_aws_embedding_model_arn
                ]
            }
        ]
    }

    kb_aws_bedrock_policy_json = json.dumps(bedrock_kb_aws_allow_fm_model_policy_statement)

    kb_aws_bedrock_policy = iam_client.create_policy(
        PolicyName=kb_aws_bedrock_allow_policy_name,
        PolicyDocument=kb_aws_bedrock_policy_json
    )


    # Create IAM policies for KB to access OpenSearch Serverless
    bedrock_kb_aws_allow_aoss_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "aoss:APIAccessAll",
                "Resource": [
                    f"arn:aws:aoss:{region}:{account_id}:collection/*"
                ]
            }
        ]
    }


    kb_aws_aoss_policy_json = json.dumps(bedrock_kb_aws_allow_aoss_policy_statement)

    kb_aws_aoss_policy = iam_client.create_policy(
        PolicyName=kb_aws_aoss_allow_policy_name,
        PolicyDocument=kb_aws_aoss_policy_json
    )


    kb_aws_s3_allow_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowKBAccessDocuments",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}/*",
                    f"arn:aws:s3:::{bucket_name}"
                ],
                "Condition": {
                    "StringEquals": {
                        "aws:ResourceAccount": f"{account_id}"
                    }
                }
            }
        ]
    }


    kb_aws_s3_json = json.dumps(kb_aws_s3_allow_policy_statement)
    kb_aws_s3_policy = iam_client.create_policy(
        PolicyName=kb_aws_s3_allow_policy_name,
        PolicyDocument=kb_aws_s3_json
    )


    # Create IAM Role for the agent and attach IAM policies
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [{
              "Effect": "Allow",
              "Principal": {
                "Service": "bedrock.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
        }]
    }

    assume_role_policy_document_json = json.dumps(assume_role_policy_document)
    kb_aws_role = iam_client.create_role(
        RoleName=kb_aws_role_name,
        AssumeRolePolicyDocument=assume_role_policy_document_json
    )

    # Pause to make sure role is created
    time.sleep(20)

    iam_client.attach_role_policy(
        RoleName=kb_aws_role_name,
        PolicyArn=kb_aws_bedrock_policy['Policy']['Arn']
    )

    iam_client.attach_role_policy(
        RoleName=kb_aws_role_name,
        PolicyArn=kb_aws_aoss_policy['Policy']['Arn']
    )

    iam_client.attach_role_policy(
        RoleName=kb_aws_role_name,
        PolicyArn=kb_aws_s3_policy['Policy']['Arn']
    )


    kb_aws_role_arn = kb_aws_role["Role"]["Arn"]
    kb_aws_role_arn


    # #### Create Vector Data Base
    # 
    # First of all we have to create a vector store. In this section we will use *Amazon OpenSerach serverless.*
    # 
    # Amazon OpenSearch Serverless is a serverless option in Amazon OpenSearch Service (AOSS). As a developer, you can use OpenSearch Serverless to run petabyte-scale workloads without configuring, managing, and scaling OpenSearch clusters. You get the same interactive millisecond response times as OpenSearch Service with the simplicity of a serverless environment. Pay only for what you use by automatically scaling resources to provide the right amount of capacity for your application—without impacting data ingestion.


    # Create OpenSearch Collection
    security_policy_json = {
        "Rules": [
            {
                "ResourceType": "collection",
                "Resource":[
                    f"collection/{kb_aws_collection_name}"
                ]
            }
        ],
        "AWSOwnedKey": True
    }
    security_policy = open_search_serverless_client.create_security_policy(
        description='security policy of aoss collection',
        name=kb_aws_collection_name,
        policy=json.dumps(security_policy_json),
        type='encryption'
    )


    kb_aws_network_policy_json = [
      {
        "Rules": [
          {
            "Resource": [
              f"collection/{kb_aws_collection_name}"
            ],
            "ResourceType": "dashboard"
          },
          {
            "Resource": [
              f"collection/{kb_aws_collection_name}"
            ],
            "ResourceType": "collection"
          }
        ],
        "AllowFromPublic": True
      }
    ]

    kb_aws_network_policy = open_search_serverless_client.create_security_policy(
        description='network policy of aoss collection',
        name=kb_aws_collection_name,
        policy=json.dumps(kb_aws_network_policy_json),
        type='network'
    )

    response = sts_client.get_caller_identity()
    current_role = response['Arn']
    logger.debug(f"current_role :: {current_role} ")
    
    kb_aws_data_policy_json = [
      {
        "Rules": [
          {
            "Resource": [
              f"collection/{kb_aws_collection_name}"
            ],
            "Permission": [
              "aoss:DescribeCollectionItems",
              "aoss:CreateCollectionItems",
              "aoss:UpdateCollectionItems",
              "aoss:DeleteCollectionItems"
            ],
            "ResourceType": "collection"
          },
          {
            "Resource": [
              f"index/{kb_aws_collection_name}/*"
            ],
            "Permission": [
                "aoss:CreateIndex",
                "aoss:DeleteIndex",
                "aoss:UpdateIndex",
                "aoss:DescribeIndex",
                "aoss:ReadDocument",
                "aoss:WriteDocument"
            ],
            "ResourceType": "index"
          }
        ],
        "Principal": [
            kb_aws_role_arn,
            f"arn:aws:sts::{account_id}:assumed-role/Admin/*",
            current_role
        ],
        "Description": ""
      }
    ]

    kb_aws_data_policy = open_search_serverless_client.create_access_policy(
        description='data access policy for aoss collection',
        name=kb_aws_collection_name,
        policy=json.dumps(kb_aws_data_policy_json),
        type='data'
    )


    kb_aws_opensearch_collection_response = open_search_serverless_client.create_collection(
        description='OpenSearch collection for Amazon Bedrock Knowledge Base for Northwind DB',
        name=kb_aws_collection_name,
        standbyReplicas='DISABLED',
        type='VECTORSEARCH'
    )
    logger.debug(f"kb_aws_opensearch_collection_response :: {kb_aws_opensearch_collection_response} ")

    kb_aws_collection_arn = kb_aws_opensearch_collection_response["createCollectionDetail"]["arn"]
    logger.debug(f"kb_aws_collection_arn :: {kb_aws_collection_arn} ")
    

    # wait for collection creation
    response = open_search_serverless_client.batch_get_collection(names=[kb_aws_collection_name])
    # Periodically check collection status
    while (response['collectionDetails'][0]['status']) == 'CREATING':
        print('Creating collection...')
        time.sleep(30)
        response = open_search_serverless_client.batch_get_collection(names=[kb_aws_collection_name])
    print('\nCollection successfully created:')
    print(response["collectionDetails"])
    # Extract the collection endpoint from the response
    host = (response['collectionDetails'][0]['collectionEndpoint'])
    final_host = host.replace("https://", "")
    logger.debug(f"final_host :: {final_host} ")


    # #### Create OpenSearch Index
    # 
    # Let's now create a vector index to index our data


    credentials = boto3.Session().get_credentials()
    service = 'aoss'
    awsauth = AWS4Auth(
        credentials.access_key, 
        credentials.secret_key,
        region, 
        service, 
        session_token=credentials.token
    )

    # Build the OpenSearch client
    open_search_client = OpenSearch(
        hosts=[{'host': final_host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=300
    )
    # It can take up to a minute for data access rules to be enforced
    time.sleep(45)
    index_body = {
        "settings": {
            "index.knn": True,
            "number_of_shards": 1,
            "knn.algo_param.ef_search": 512,
            "number_of_replicas": 0,
        },
        "mappings": {
            "properties": {}
        }
    }

    index_body["mappings"]["properties"][kb_aws_vectorField] = {
        "type": "knn_vector",
        "dimension": 1536,
        "method": {
            "name": "hnsw",
            "engine": "faiss",
            "space_type": "innerproduct",
            "parameters": {
                "ef_construction": 512, 
                "m": 16
            },
        },
    }

    index_body["mappings"]["properties"][kb_aws_textField] = {
        "type": "text"
    }

    index_body["mappings"]["properties"][kb_aws_metadataField] = {
        "type": "text"
    }

    # Create index
    response = open_search_client.indices.create(kb_aws_vector_index_name, body=index_body)
    print('\nCreating index:')
    logger.debug(f"response :: {response} ")


    kb_aws_storage_configuration = {
        'opensearchServerlessConfiguration': {
            'collectionArn': kb_aws_collection_arn, 
            'fieldMapping': {
                'metadataField': kb_aws_metadataField,
                'textField': kb_aws_textField,
                'vectorField': kb_aws_vectorField
            },
            'vectorIndexName': kb_aws_vector_index_name
        },
        'type': 'OPENSEARCH_SERVERLESS'
    }


    # Creating the knowledge base
    try:
        # ensure the index is created and available
        time.sleep(45)
        kb_aws_obj = bedrock_agent_client.create_knowledge_base(
            name=kb_aws_name, 
            description='KB that contains information to provide accurate responses on building software applications based on the AWS best practices and AWS well-architected framework',
            roleArn=kb_aws_role_arn,
            knowledgeBaseConfiguration={
                'type': 'VECTOR',  # Corrected type
                'vectorKnowledgeBaseConfiguration': {
                    'embeddingModelArn': kb_aws_embedding_model_arn
                }
            },
            storageConfiguration=kb_aws_storage_configuration
        )

        # Pretty print the response
        #pprint.pprint(kb_aws_obj)
        logger.debug(f"kb_aws_obj :: {kb_aws_obj} ")

    except Exception as e:
        print(f"Error occurred: {e}")


    # #### Create a data source that you can attach to the recently created Knowledge Base
    # 
    # Let's create a data source for our Knowledge Base. Then we will ingest our data and convert it into embeddings.


    # Define the S3 configuration for your data source
    s3_configuration = {
        'bucketArn': bucket_arn,
        'inclusionPrefixes': [kb_aws_key]  
    }

    # Define the data source configuration
    kb_aws_data_source_configuration = {
        's3Configuration': s3_configuration,
        'type': 'S3'
    }

    knowledge_base_aws_id = kb_aws_obj["knowledgeBase"]["knowledgeBaseId"]
    knowledge_base_aws_arn = kb_aws_obj["knowledgeBase"]["knowledgeBaseArn"]


    kb_aws_chunking_strategy_configuration = {
        "chunkingStrategy": "FIXED_SIZE",
        "fixedSizeChunkingConfiguration": {
            "maxTokens": 1024,
            "overlapPercentage": 50
        }
    }


    # Create the data source
    try:
        # ensure that the KB is created and available
        time.sleep(45)
        kb_aws_data_source_response = bedrock_agent_client.create_data_source(
            knowledgeBaseId=knowledge_base_aws_id,
            name=kb_aws_data_source_name,
            description='DataSource for the AWS well architected framework',
            dataSourceConfiguration=kb_aws_data_source_configuration,
            vectorIngestionConfiguration = {
                "chunkingConfiguration": kb_aws_chunking_strategy_configuration
            }
        )

        # Pretty print the response
        logger.debug(f"kb_aws_data_source_response :: {kb_aws_data_source_response} ")

    except Exception as e:
        print(f"Error occurred: {e}")


    # #### Start ingestion job
    # Once the Knowledge Base and Data Source are created, we can start the ingestion job.
    # During the ingestion job, Knowledge Base will fetch the documents in the data source, pre-process it to extract text, chunk it based on the chunking size provided, create embeddings of each chunk and then write it to the vector database, in this case Amazon OpenSource Serverless.



    # Start an ingestion job
    kb_aws_data_source_id = kb_aws_data_source_response["dataSource"]["dataSourceId"]
    start_job_response = bedrock_agent_client.start_ingestion_job(
        knowledgeBaseId=knowledge_base_aws_id, 
        dataSourceId=kb_aws_data_source_id
    )


    # ### <a name="7">Create Agent</a>
    # (<a href="#0">Go to top</a>)
    # 
    # 
    # We will now create our agent. To do so, we first need to create the agent policies that allow bedrock model invocation  and s3 bucket access. 
#foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
#"anthropic.claude-v2"
# amazon.titan-text-premier-v1:0

    # Create IAM policies for agent
    bedrock_agent_bedrock_allow_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AmazonBedrockAgentBedrockFoundationModelPolicy",
                "Effect": "Allow",
                "Action": "bedrock:InvokeModel",
                "Resource": [
                    f"arn:aws:bedrock:{region}::foundation-model/anthropic.claude-v2"
                ]
            }
        ]
    }

    bedrock_policy_json = json.dumps(bedrock_agent_bedrock_allow_policy_statement)

    agent_bedrock_policy = iam_client.create_policy(
        PolicyName=bedrock_agent_bedrock_allow_policy_name,
        PolicyDocument=bedrock_policy_json
    )


    bedrock_agent_s3_allow_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowAgentAccessOpenAPISchema",
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": [
                    schema_arn
                ]
            }
        ]
    }


    bedrock_agent_s3_json = json.dumps(bedrock_agent_s3_allow_policy_statement)
    agent_s3_schema_policy = iam_client.create_policy(
        PolicyName=bedrock_agent_s3_allow_policy_name,
        Description=f"Policy to allow invoke Lambda that was provisioned for it.",
        PolicyDocument=bedrock_agent_s3_json
    )


    # ### Make sure KB retreival IAM policy includes both DB and AWS arns


    bedrock_agent_kb_retrieval_policy_statement = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "bedrock:Retrieve"
                ],
                "Resource": [
                    knowledge_base_db_arn,
                    knowledge_base_aws_arn
                ]
            }
        ]
    }
    bedrock_agent_kb_json = json.dumps(bedrock_agent_kb_retrieval_policy_statement)
    agent_kb_schema_policy = iam_client.create_policy(
        PolicyName=bedrock_agent_kb_allow_policy_name,
        Description=f"Policy to allow agent to retrieve documents from knowledge base.",
        PolicyDocument=bedrock_agent_kb_json
    )


    # Create IAM Role for the agent and attach IAM policies
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [{
              "Effect": "Allow",
              "Principal": {
                "Service": "bedrock.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
        }]
    }

    assume_role_policy_document_json = json.dumps(assume_role_policy_document)
    agent_role = iam_client.create_role(
        RoleName=agent_role_name,
        AssumeRolePolicyDocument=assume_role_policy_document_json
    )
    
    logger.debug(f"agent_name :: {agent_name}  >>>>>  agent_role :: {agent_role}")

    # Pause to make sure role is created
    time.sleep(20)

    iam_client.attach_role_policy(
        RoleName=agent_role_name,
        PolicyArn=agent_bedrock_policy['Policy']['Arn']
    )

    iam_client.attach_role_policy(
        RoleName=agent_role_name,
        PolicyArn=agent_s3_schema_policy['Policy']['Arn']
    )

    iam_client.attach_role_policy(
        RoleName=agent_role_name,
        PolicyArn=agent_kb_schema_policy['Policy']['Arn']
    )

    logger.info(f"agent_name :: {agent_name} \n agent_alias_name :: {agent_alias_name} \n agent_role :: {agent_role} \n bucket_name :: {bucket_name} \n schema_key :: {schema_key} \n knowledge_base_db_id :: {knowledge_base_db_id} \n knowledge_base_aws_id :: {knowledge_base_aws_id} ")
    
    logger.info(f"agent_name :: {agent_name} \n agent_alias_name :: {agent_alias_name} \n bucket_name :: {bucket_name} \n schema_key :: {schema_key} \n knowledge_base_db_id :: {knowledge_base_db_id} ")
    
    infra_response = {
        "agent_name": agent_name,
        "agent_alias_name": agent_alias_name,
        "agent_role": agent_role,
        "bucket_name": bucket_name,
        "schema_key": schema_key,
        "knowledge_base_db_id": knowledge_base_db_id,
        "knowledge_base_aws_id": knowledge_base_aws_id,
        "lambda_name": lambda_name,
        "lambda_function": lambda_function,
        "agent_bedrock_policy": agent_bedrock_policy,
        "agent_s3_schema_policy": agent_s3_schema_policy,
        "agent_role_name": agent_role_name,
        "lambda_role_name": lambda_role_name,
        "kb_db_collection_name": kb_db_collection_name,
        "kb_aws_collection_name": kb_aws_collection_name,
        "agent_kb_schema_policy": agent_kb_schema_policy,
        "kb_db_bedrock_policy": kb_db_bedrock_policy,
        "kb_db_aoss_policy": kb_db_aoss_policy,
        "kb_db_s3_policy": kb_db_s3_policy,
        "kb_db_role_name": kb_db_role_name,
        "kb_db_opensearch_collection_response": kb_db_opensearch_collection_response,
        "kb_aws_bedrock_policy": kb_aws_bedrock_policy,
        "kb_aws_aoss_policy": kb_aws_aoss_policy,
        "kb_aws_s3_policy": kb_aws_s3_policy,
        "kb_aws_role_name": kb_aws_role_name,
        "kb_aws_opensearch_collection_response": kb_aws_opensearch_collection_response
    }

    return infra_response

    
    return agent_name, agent_alias_name, agent_role, bucket_name, schema_key, knowledge_base_db_id, knowledge_base_aws_id, lambda_name, lambda_function, kb_db_name, kb_aws_name



def cleanup_infrastructure(agent_action_group_response, lambda_name, lambda_function, lambda_role_name, agent_id, agent_alias_id, agent_role_name, bucket_name, schema_key, agent_bedrock_policy, agent_s3_schema_policy, agent_kb_schema_policy, kb_db_bedrock_policy, kb_db_aoss_policy, kb_db_s3_policy, kb_db_role_name, kb_db_collection_name, kb_db_opensearch_collection_response, knowledge_base_db_id, kb_aws_bedrock_policy, kb_aws_aoss_policy, kb_aws_s3_policy, kb_aws_role_name, kb_aws_collection_name, kb_aws_opensearch_collection_response, knowledge_base_aws_id):


    # 
    # The next steps are optional and demonstrate how to delete our agent. To delete the agent we need to:
    # 1. update the action group to disable it
    # 2. delete agent action group
    # 3. delete agent alias
    # 4. delete agent
    # 5. delete lambda function
    # 6. empty created s3 bucket
    # 7. delete s3 bucket


    # This is not needed, you can delete agent successfully after deleting alias only
    # Additionaly, you need to disable it first

    action_group_id = agent_action_group_response['agentActionGroup']['actionGroupId']
    action_group_name = agent_action_group_response['agentActionGroup']['actionGroupName']

    response = bedrock_agent_client.update_agent_action_group(
       agentId=agent_id,
       agentVersion='DRAFT',
       actionGroupId= action_group_id,
       actionGroupName=action_group_name,
       actionGroupExecutor={
           'lambda': lambda_function['FunctionArn']
       },
       apiSchema={

           's3': {
               's3BucketName': bucket_name,
               's3ObjectKey': schema_key
           }
       },
       actionGroupState='DISABLED',
    )

    action_group_deletion = bedrock_agent_client.delete_agent_action_group(
       agentId=agent_id,
       agentVersion='DRAFT',
       actionGroupId= action_group_id
    )


    agent_alias_deletion = bedrock_agent_client.delete_agent_alias(
        agentId=agent_id,
        agentAliasId=agent_alias_id
    )



    agent_deletion = bedrock_agent_client.delete_agent(
        agentId=agent_id
    )


    # Delete Lambda function
    lambda_client.delete_function(
        FunctionName=lambda_name
    )


    

    #agent_s3_schema_policy


    # Delete IAM Roles and policies

    for policy in [
        agent_bedrock_policy, 
        agent_s3_schema_policy, 
        agent_kb_schema_policy,
        kb_db_bedrock_policy,
        kb_aws_bedrock_policy,
        kb_db_aoss_policy,
        kb_aws_aoss_policy,
        kb_db_s3_policy,
        kb_aws_s3_policy
    ]:
        response = iam_client.list_entities_for_policy(
            PolicyArn=policy['Policy']['Arn'],
            EntityFilter='Role'
        )

        for role in response['PolicyRoles']:
            iam_client.detach_role_policy(
                RoleName=role['RoleName'], 
                PolicyArn=policy['Policy']['Arn']
            )

        iam_client.delete_policy(
            PolicyArn=policy['Policy']['Arn']
        )


    iam_client.detach_role_policy(RoleName=lambda_role_name, PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')
    iam_client.detach_role_policy(RoleName=lambda_role_name, PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess')

    for role_name in [
        agent_role_name, 
        lambda_role_name, 
        kb_db_role_name,
        kb_aws_role_name
    ]:
        try: 
            iam_client.delete_role(
                RoleName=role_name
            )
        except Exception as e:
            print(e)
            print("couldn't delete role", role_name)

    try:

        open_search_serverless_client.delete_collection(
            id=kb_db_opensearch_collection_response["createCollectionDetail"]["id"]
        )

        open_search_serverless_client.delete_collection(
            id=kb_aws_opensearch_collection_response["createCollectionDetail"]["id"]
        )

        open_search_serverless_client.delete_access_policy(
              name=kb_db_collection_name,
              type='data'
        )

        open_search_serverless_client.delete_security_policy(
              name=kb_db_collection_name,
              type='network'
        )

        open_search_serverless_client.delete_security_policy(
              name=kb_db_collection_name,
              type='encryption'
        )

        bedrock_agent_client.delete_knowledge_base(
            knowledgeBaseId=knowledge_base_db_id
        )


        open_search_serverless_client.delete_access_policy(
              name=kb_aws_collection_name,
              type='data'
        )

        open_search_serverless_client.delete_security_policy(
              name=kb_aws_collection_name,
              type='network'
        )

        open_search_serverless_client.delete_security_policy(
              name=kb_aws_collection_name,
              type='encryption'
        )

        bedrock_agent_client.delete_knowledge_base(
            knowledgeBaseId=knowledge_base_aws_id
        )

    except Exception as e:
        print(e)

    '''
    # Empty and delete S3 Bucket
    print(f"Empty and delete bucket_name ::: {bucket_name}")

    objects = s3_client.list_objects(Bucket=bucket_name)  
    if 'Contents' in objects:
        for obj in objects['Contents']:
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
    time.sleep(40)
    s3_client.delete_bucket(Bucket=bucket_name)
    '''


    print(f"Cleanup completed >>>>>>>>>> ")
