# System Module
import json
import logging
import os
import sys

# 3rd Party Module
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        passwd=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        connect_timeout=10,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
except pymysql.MySQLError as e:
    logger.error('ERROR: Could not connect to MariaDB instance.')
    logger.error(e)
    sys.exit()

logger.info('SUCCESS: Connection to RDS MariaDB instance succeeded')

SQL_STMT = """
SELECT cepage,
       color,
       comment,
       country,
       name,
       name_jpn,
       producer,
       producer_jpn,
       region,
       region_jpn,
       vintage
  FROM wines
 ORDER BY color, producer, name
"""
 
def lambda_handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
    entities = []
    with conn.cursor() as cursor:
        cursor.execute(SQL_STMT)
        entities = cursor.fetchall()
    return {
        'statusCode': 200,
        'body': json.dumps(entities)
    }
