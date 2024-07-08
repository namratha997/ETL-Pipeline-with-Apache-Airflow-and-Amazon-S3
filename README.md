# ETL Pipeline with Apache Airflow and Amazon-S3

## Project Overview
This project focuses on developing an end-to-end ETL (Extract, Transform, Load) pipeline using Apache Airflow and Amazon S3. This pipeline will fetch weather data from the OpenWeather API, transform it into a structured format, and load it into an S3 bucket. By the end of this project, you will have a fully functional pipeline that can be scheduled to run at your desired frequency.

## Project Structure
1. Fetch Weather Data: Retrieve weather data from the OpenWeather API.
2. Transform Weather Data: The data fetched from the API is in JSON format, the transform includes creating a dataframe from the JSON object and converting the dataframe to a CSV file
3. Load Data to S3: Store the transformed data in an S3 bucket.

## Tools and libraries Used
1. Apache Airflow: A powerful and flexible platform to programmatically author, schedule, and monitor workflows.
2. OpenWeather API: A service that provides weather data for various cities.
3. Amazon S3: A scalable object storage service from Amazon Web Services (AWS).
4. Pandas: A Python library used for data manipulation and analysis.
5. Boto3: The AWS SDK for Python, which allows Python developers to write software that makes use of Amazon services like S3.

## Process
Connect the OpenWeather API and fetch the data. We use python to transform data, deploy the code on Airflow/EC2 and save the final result on Amazon S3.
1. Write a script to connect the API and fetch the data. Store the data in a dataframe.
2. Create an EC2 instance, start the instance and connect it to the console. I have used free-tier AWS to create this instance. The specs include t2.micro and ubantu 22 version.
3. Once the instance starts running, connect it to the console and install the following:
   - sudo apt-get update
   - sudo install python3-pip
   - sudo pip install apache-airflow
   - sudo pip install pandas
   - sudo pip install s3fs
   - sudo pip install pyarrow
   - sudo pip install requests
   - sudo pip install boto3
4. Once this is installed, check if the airflow has been installed right. Use command airflow to check this. Run "airflow standalone" running this command will give the initial credentials. Copy and paste the credentials to use it later.
5. In the active running instance, go to security and access the security group. Edit the inbound rules and create a new role. Set it to "all traffic", "anywhere IPv4".  
7. Run the airflow server and scheduler using- airflow scheduler & airflow webserver --port 8080 & [port 8080 is what I'm using]
8. Copy the public IP address add the port ex: 172.31.22.254:8080. This will open the airflow application. Use the default credentials to login and reset the password to one liking.
9. In AWS, create an S3 bucket to store the data. Adjust the permissions using IAM role. Create a new IAM role and give permissions tp S3 and EC2.
10. In the python code, add the relevant S3 bucket name and save it.
11. In the instance console stop the server and run the commands.
   - airflow
   - cd airflow
   - ls
   - sudo nano airflow.cfg
   - In the dags folder, adjust the file name. Save the modified buffer and exit.
12. Once the file is saved, re-run the airflow commands and login. You should be able to see the Dag file inside the airflow.
13. Click and open the file and you should be able to run it manually. Once it runs successfully, the data should be visisble in S3 bucket.

Here's how the Airflow UI looks like
![Airflow Interface-DAG](https://github.com/namratha997/ETL-Pipeline-with-Apache-Airflow-and-Amazon-S3/blob/main/Picture1.png)
![Airflow Project UI](https://github.com/namratha997/ETL-Pipeline-with-Apache-Airflow-and-Amazon-S3/blob/main/Picture2.png)
![Graph](https://github.com/namratha997/ETL-Pipeline-with-Apache-Airflow-and-Amazon-S3/blob/main/Picture3.png)
![logs](https://github.com/namratha997/ETL-Pipeline-with-Apache-Airflow-and-Amazon-S3/blob/main/Picture4.png)
   
