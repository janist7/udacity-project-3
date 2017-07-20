#!/usr/bin/env python3
''' Generates formatted report in console '''

from report import newsdb


def main():
    ''' Generates report data, prints it '''
    report_title = []
    answers_list = []
    answer_row = ""
    result = ""

    # Create lists from query results
    for report in newsdb.get_reports():
        report_title.append(report["title"])
        answers_list.append(report["answer"])

    # Add all answers for a question
    for i in range(0, len(report_title)):
        for answer in answers_list[i]:
            answer_row += str(answer[0]) + " - " + str(answer[1]) + "\n"
        result += "\n" + report_title[i] + "\n\n" + answer_row
        answer_row = ""

    print(result)

''' Runs main function if file is run '''
if __name__ == '__main__':
    main()
