#!/usr/bin/env python3
''' Runs and generates report page at http://localhost:8000/report/ '''

from flask import Flask, request, redirect, url_for

import newsdb

app = Flask(__name__)

# HTML template for the report page
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
      <div><button id="go" type="submit">Regenerate Report</button></div>
    </form>
%s
  </body>
</html>
'''

# HTML template a question
QUESTION = '''\
    <h2>%s</h2>%s
'''
# HTML template a single result
ANSWER = '''\
    <p>%s</p>
'''

@app.route('/report/', methods=['GET'])
def main():
    '''Generates report page data'''
    report_title = []
    answers_list = []
    answer_row = ""
    question = ""

    # Create lists from query results
    for report in newsdb.get_reports():
        report_title.append(report["title"])
        answers_list.append(report["answer"])

    # Add all answers for a question
    for i in range(0, len(report_title)):
        for answer in answers_list[i]:
            answer_row += "".join(ANSWER %
                                  str(answer[0] + " - " + str(answer[1])))
        question += "".join(QUESTION % (report_title[i], answer_row))
        answer_row = ""
    html = HTML_WRAP % question
    return html


@app.route('/report/', methods=['POST'])
def post():
    '''Redirect to regenerate reports.'''
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
