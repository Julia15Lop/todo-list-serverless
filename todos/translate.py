import logging
import json
import boto3
import os

from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')

# Logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def translate(event, context):
    translate = boto3.client('translate')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    # Variables translate: source_language, review and target_language
    review_id = event['pathParameters']['id']
    source_language = 'auto'
    target_language = event['pathParameters']['lang']
    
    # Get item from the database by id
    result = table.get_item(
        Key={
            'id': review_id
        }
    )
        
    if 'Item' in result:
        review = result['Item']['text']
    else:
        return print("[ItemNotFound]: Input id not found")
        
    # TranslateText operation and passes values
    translated_text = translate.translate_text(Text=review,SourceLanguageCode=source_language, TargetLanguageCode=target_language)
            
    # Create response
    response = {
        "statusCode": 200,
        "body": json.dumps(translated_text["TranslatedText"] + "\n", ensure_ascii=False).encode('utf8')
    }
    return response