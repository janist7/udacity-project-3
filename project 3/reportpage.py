#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for

import newsdb

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Report</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>Report</h1>
    <form method=post>
      <div><button id="go" type="submit">Generate Report</button></div>
    </form>
%s
  </body>
</html>
'''

# HTML template for an individual comment
POST = '''\
    <h2>%s:</h2>%s
'''
POST_ANSWERS = '''\
    <p>%s</p>
'''

@app.route('/', methods=['GET'])
def main():
  '''Main page of the forum.'''
  report_title = []
  answers = []
  post_answers = ""
  posts = ""
  
  for report in newsdb.get_reports():
    report_title.append(report["title"])
    answers.append(report["answer"])

  for i in range(0,len(report_title)):
    for answer in answers[i]:
      post_answers += "".join(POST_ANSWERS % str(answer))
    posts += "".join(POST % (report_title[i],post_answers))
    post_answers = ""
  html = HTML_WRAP % posts
  return html


@app.route('/', methods=['POST'])
def post():
  '''Redirect to regenerate posts.'''
  return redirect(url_for('main'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)

