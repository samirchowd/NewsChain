import psycopg2
from psycopg2 import DatabaseError as Error
import os
import gcloud


#creates remote sql instance on google cloud
#user: postgres, password: NewsChain2021
def create_google_sql_instance():
    os.system("gcloud init")
    os.system("gcloud auth login")
    os.system("gcloud sql instances create articledb --database-version=POSTGRES_11 " +
              "--cpu=2 --memory=7680MB --region=us-east4")
    os.system("gcloud sql users set-password postgres --instance=articledb --password=NewsChain2021")

#deletes previously created google cloud sql instance
#Make sure to delete instance!
def delete_google_sql_instance():
    os.system("gcloud sql instances DELETE articledb")

# Function to establish database connection (use this for local postgres instance)
# If the connection is successful, the function returns a connection object.
def create_server_connection(host_name, user_name, user_password):

    connection = None
    try:
        connection = psycopg2.connect(
            host=host_name,
            dbname='postgres',
            user=user_name,
            password=user_password
        )

        print("Psql Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

create_google_sql_instance()
delete_google_sql_instance()




