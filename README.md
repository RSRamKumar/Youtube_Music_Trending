# Youtube Music Trending Project

![image](https://github.com/user-attachments/assets/2c4adaf4-7b94-46df-a850-b3342f1caa33)

Fig: Overview of the Project

A project to find the top trending music videos in India (or other region) by retrieving the data using the
Youtube API, parsing the relevant information and creating a simple dashboard in Plotly.

Airflow was launched using AWS EC2 instance. AWS Lambda function was utilized to trigger the transformation script that converts the parsed JSON file into a CSV file for downstream operations.
The transformed data was then crawled by Glue Crawler from S3 Bucket. Then, interactive queries were written with the help of Athena to understand and answer questions
regarding the trending.

Tools Used:
1. Python [ETL Pipeline including Pydantic for data parsing and validation],
2. Airflow on EC2 instance [Task orchestration],
3. Plotly Dash [Data Visualization]
4. Terraform [Infrastructure Definition]

![image](https://github.com/RSRamKumar/Youtube_Music_Trending/assets/39699070/15bb640d-f184-4be2-9535-0075b75d3656)


Fig: Plotly visualization stored in the desired repository. On clicking the bubbles, it directly navigates us to the youtube video.
