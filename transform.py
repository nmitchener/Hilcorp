#!/usr/bin/env python

import csv
import sys
import os

if (len(sys.argv) < 2):
    print "Usage: %s FILE..." % sys.argv[0]
    print
    print "\tProcesses FILE and outputs to current directory as file.columnar.csv"
    sys.exit(1)

files = sys.argv[1:]

TAG = 0
TS = 1
VAL = 2

for input_file in files:
    output_file = os.path.splitext(os.path.basename(input_file))[0] + ".columnar.csv"

    print "input file: %s" % input_file
    print "output file: %s" % output_file

    if (os.path.isfile(output_file)):
        print "Already done. Skipping."
        continue


    # Array of row headers: [ 'timestamp', 'tagName1', ..., 'tagNameN' ]
    headers = ['timestamp']

    # Array of tag data arrays in same order as header_data (think csv rows)
    row_data = []


    def buffer_row(buf, row):
        # NOTE - may need to cache index for performance
        tag_idx = headers.index(row[TAG])
        buf[tag_idx] = row[VAL]

    # Parse entire CSV to get complete tag list
    sys.stdout.write("Scanning for exhaustive tag list... ")
    sys.stdout.flush()
    with open(input_file) as csvfile:
        header_reader = csv.reader(csvfile)
        for row in header_reader:
            if (row[TAG] not in headers):
                headers.append(row[TAG])
    print 'done.'
    print 'Found %d tags' % (len(headers)-1) # -1 for timestamp

    # Re-process for data
    with open(input_file) as csvfile:
        reader = csv.reader(csvfile)

        # Must pre-allocate buffer for buf[i] access
        buf = [None] * len(headers)

        # Process first row out of loop to set initial timestamp
        first_row = reader.next()
        buf[0] = first_row[TS]
        buffer_row(buf, first_row)

        for row in reader:
            # New row
            if (buf[0] != row[TS]):
                # flush row buf to row_data
                row_data.append(buf)
                # allocate new buf since row_data is pointing to the old one
                buf = list(buf)

                # set timestamp as first element of new row
                buf[0] = row[TS]
                sys.stdout.write('Reading data from %s\r' % row[TS])
                sys.stdout.flush()

            buffer_row(buf, row)

        # write last row
        row_data.append(buf)
        print

    print 'Writing output to %s' % output_file
    with open(output_file, 'w') as csvfile:
        w = csv.writer(csvfile)
        w.writerow(headers)

        for row in row_data:
            sys.stdout.write('Writing data from %s\r' % row[0])
            sys.stdout.flush()
            w.writerow(row)

        print

    print "Total Timestamps: %d" % len(row_data)

    # Number of tags to print at the end
    print_tag_count = 4
    # Number of rows to print
    print_row_count = 20

    print "First %d tags in %d rows:" % (print_tag_count, print_row_count)

    # Print first 10 tags
    tags = headers[1:print_tag_count+1]
    pad = "%23s"

    buf = [pad % "timestamp"]
    for t in tags:
        buf.append(pad % t)
    print "|".join(buf)

    # Print first 30 rows
    for i in range(0,print_row_count):
        buf = [pad % row_data[i][0]]
        for t in tags:
            tag_idx = headers.index(t)
            buf.append(pad % row_data[i][tag_idx])
        print "|".join(buf)
