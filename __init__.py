import re
import csv
from tkinter import *
from tkinter import filedialog

file_lines = None


def main():
    global file_lines
    survey_stats = ''
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("CSV files", "*.csv")])
    try:
        _file = open(path, newline='')
    except FileNotFoundError:
        print("ERR: The file does not exist")
        quit()
    csv_file = csv.reader(_file)
    file_lines = []
    while 1:
        try:
            file_lines.append(next(csv_file))
        except StopIteration:
            break
    file_lines.pop(1)   # Remove second line of csv
    preview_count = 2
    while preview_count < len(file_lines):
        if file_lines[preview_count][2] == "Survey Preview":    # Remove previews
            file_lines.pop(preview_count)
        else:
            preview_count += 1
    for column in range(21, len(file_lines[0])):
        survey_stats += get_letters(column) + " " + file_lines[0][column] + ", Mean: " + get_average(column) + '\n'

    stats_name = path.split('/')[-1].split('.')[0]
    final_file = open(stats_name + ".txt", "w")
    final_file.write(survey_stats)
    final_file.close()
    quit()


def get_average(column):
    global file_lines
    total = 0.0
    num_responses = 0.0
    for line in file_lines:
        val = line[column]
        if re.match(r"^\d+$", val):
            total += float(val)
            num_responses += 1
    if not num_responses:
        return str(0)
    return str(total / num_responses)


def get_letters(value):
    if value < 26:
        return chr(value + 65)
    else:
        return chr(int(value / 26)+64) + chr(int(value % 26)+65)


main()
