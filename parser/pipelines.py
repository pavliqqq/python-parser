import logging

from dotenv import load_dotenv
import os

import mysql.connector
import time


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ParserPipeline:
    def __init__(self):
        load_dotenv()
        
        self.conn = mysql.connector.connect(
            database = os.getenv('DB_NAME'),
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD')
        )

        self.qa_table = 'question_answer'
        self.answers_table = 'answers'
        self.question_table = 'questions'

    def process_item(self, item, spider):
        try:
            rows = item['data_rows']

            columns = list(rows[0].keys())
            questionColumn = columns[0]
            answerColumn = columns[1]

            inserted_count = 0
            
            with self.conn.cursor() as cursor:
                for row in rows:
                    question_text = row[questionColumn]
                    answer_text = row[answerColumn]

                    question_id = self.get_id(cursor, self.question_table, questionColumn, question_text)
                    answer_id = self.get_id(cursor, self.answers_table, answerColumn, answer_text)

                    data = {
                        'question_id': question_id,
                        'answer_id': answer_id,
                    }

                    inserted_count += self.link_question_to_answer(cursor, data)

                self.conn.commit()
            logging.info("Insert data: expected: %s, inserted: %s", len(rows), inserted_count)
        except Exception as e:
            self.conn.rollback()
            logging.error("Insert data error: %s", e)
            raise

    def get_id(self, cursor, table, column, value):
        query = f"SELECT id FROM {table} WHERE {column} = %s"
        cursor.execute(query, (value,))
        row = cursor.fetchone()

        if row is None:
                return self.insert_data(cursor, table, column, value)
            
        return row[0]
    
    def insert_data(self, cursor, table, column, value):
        query = f"INSERT INTO {table} ({column}) VALUES (%s)"
        cursor.execute(query, (value,))

        return cursor.lastrowid

    def link_question_to_answer(self, cursor, data):
        columns = list(data.keys())
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"""
            INSERT IGNORE INTO {self.qa_table}
            ({", ".join(columns)})
            VALUES ({placeholders})
        """

        values = list(data.values())
        cursor.execute(query, values)

        return cursor.rowcount

    def close_spider(self, spider):
        self.conn.close()