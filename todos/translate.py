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
    
    source_language = 'auto'
    
    # Get item from the database by id
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
        
    if 'Item' in result:
        review = result['Item']['text']
    else:
        return print("[ItemNotFound]: Input id not found")
        
    # TranslateText operation and passes values
    translation = translate.translate_text(Text=review,SourceLanguageCode=source_language, TargetLanguageCode=event['pathParameters']['lang'])
            
    # create response
    response = {
        "statusCode": 200,
        "body": json.dumps(translation["TranslatedText"], cls=decimalencoder.DecimalEncoder)
    }
    return response
        
#         except Exception as e:
#             logger.error(result)
#             raise Exception("[ErrorMessage]: " + str(e))
            
#         try:
#          # The Lambda function calls the TranslateText operation and passes the
#          # review, the source language, and the target language to get the
#          # translated review.
#             result = translate.translate_text(Text=review,
#             SourceLanguageCode=source_language, TargetLanguageCode=target_language)
#             logging.info("Translation output: " + str(result))
#         except Exception as e:
#             logger.error(response)
#             raise Exception("[ErrorMessage]: " + str(e))
        
#         try:
#         # After the review is translated, the function stores it using
#         # the Amazon DynamoDB putItem operation. Subsequent requests
#         # for this translated review are returned from Amazon DynamoDB.
#             response = dynamodb.put_item(
#                 TableName=table,
#                 Item={
#                     'review_id': {
#                         'N': review_id,
#                     },
#                     'language': {
#                         'S': target_language,
#                     },
#                     'review': {
#                         'S': result.get('TranslatedText')
#                     }
#                 }
#             )
#             logger.info(response)
#         except Exception as e:
#             logger.error(e)
#             raise Exception("[ErrorMessage]: " + str(e))
#         return result.get('TranslatedText')