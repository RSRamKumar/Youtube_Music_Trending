import json
import boto3
import pandas as pd

def lambda_handler(event, context):
    """
    Lambda function to transform of Youtube Results
    JSON file to CSV file
    """
   
    # Parse Bucket Name, File Name
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    json_file_name = event['Records'][0]['s3']['object']['key']
    
    
    # Connect to S3 and Get the JSON
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket_name, Key=json_file_name)
    json_content = response['Body'].read().decode('utf-8')
    
    # JSON To CSV Transformation
    individual_result_list = []
    json_data = json.loads(json_content)
    for result in json_data:
        individual_result_list.append(
            {
                **result["snippet"],
                **result["contentDetails"],
                **result["statistics"],
                **{"video_url": result["video_url"]},
            })
          
    df_csv = pd.DataFrame(individual_result_list)
    csv_file_name = json_file_name.replace('json', 'csv')
    df_csv = df_csv.to_csv(index=False)
    
    # Writing the CSV file to S3 Bucket
    s3_client.put_object(Bucket= 'youtube-data-bucket-ram-transformed-data', Key=csv_file_name, Body=df_csv)
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('JSON is successfully transormed into a CSV file')
    }
