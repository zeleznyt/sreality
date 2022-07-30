#!/usr/bin/env python3

import http.server
import socketserver

from sqlalchemy import create_engine, inspect
import os
import pandas as pd
import time

DB_USER = os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASS']
DB_HOST = os.environ['POSTGRES_HOST']
DB_PORT = os.environ['POSTGRES_PORT']
DB_NAME = os.environ['POSTGRES_DB']
db_string = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(db_string)

time.sleep(45)

df = pd.read_sql_query('SELECT * FROM realities', con=engine)

sreality_content = df.to_dict()

html_content = ''
for i, image in enumerate(sreality_content['title']):
    print(sreality_content['title'][i])
    html_title = '<h3>{}</h3>'.format(sreality_content['title'][i])
    html_image = '<img src="{}" alt="{}">'.format(sreality_content['image'][i], sreality_content['title'][i])

    html_content += '<p>' + html_title + html_image + '</p><hr>'

html_template = '<html><body><meta charset="UTF-8"><h1>sreality.cz</h1>{}</body></html>'.format(html_content)

class SimpleHTTP(http.server.BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

    self.wfile.write(bytes(html_template, 'utf-8'))

  def do_POST(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()


with socketserver.TCPServer(("", 8080), SimpleHTTP) as httpd:
  httpd.serve_forever()
