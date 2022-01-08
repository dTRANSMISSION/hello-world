from flask import Flask
import boto3
import pymysql
import json
import os
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

secretsmanager = boto3.client('secretsmanager')
secrets = json.loads(secretsmanager.get_secret_value(
    SecretId=os.environ['RDS_SECRET_ARN']
)['SecretString'])
db_username  = secrets['username']
db_password  = secrets['password']
db_endpoint  = os.environ['DB_HOST']
db_name      = secrets['dbname']
target_table = "app"
content_str  = "Hello World"

@app.route("/")
def index():
    # Connect to the RDS Instance
    try:
        conn = pymysql.connect(host=db_endpoint,
                               user=db_username,
                               password=db_password,
                               database=db_name,
                               port=3306,
                               connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error(f"Could not connect to MySQL instance: {db_endpoint}")
        logger.error(e)
        sys.exit()
    logger.info(f"Connection to RDS MySQL instance succeeded: {db_endpoint}")
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {target_table} WHERE content = '{content_str}'")
        data = cur.fetchone()

    conn.close()
    logger.info(f"Connection to {db_endpoint}:{db_name} closed")
    return f"<h1 style='text-align:center' style='font-size:10vw'>{data[1]}</h1>"

@app.route("/in/sert")
def insert():
    # Connect to the RDS Instance
    try:
        conn = pymysql.connect(host=db_endpoint,
                               user=db_username,
                               password=db_password,
                               database=db_name,
                               port=3306,
                               connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error(f"Could not connect to MySQL instance: {db_endpoint}")
        logger.error(e)
        sys.exit()
    logger.info(f"Connection to RDS MySQL instance succeeded: {db_endpoint}")

    with conn.cursor() as cur:
        cur.execute(f"DROP TABLE IF EXISTS {target_table}")
        cur.execute(f"""CREATE TABLE {target_table} (`id` int(11) NOT NULL AUTO_INCREMENT,
                                                     `content` varchar(255) DEFAULT '',
                                                     PRIMARY KEY (`id`)) DEFAULT CHARSET=utf8""")
        cur.execute(f"""INSERT INTO {target_table} (content)
                    VALUES ('{content_str}')""")
        conn.commit()
        logger.info(f"INSERT commit to {target_table} complete")

    conn.close()
    logger.info(f"Connection to {db_endpoint}:{db_name} closed")
    return f"<h1 style='text-align:center' style='font-size:10vw'>{db_endpoint}:{db_name} Updated</h1>"

@app.route("/hello")
def hello_world():
    return "<h1 style='text-align:center' style='font-size:10vw'>Hello, Static World!</h1>"