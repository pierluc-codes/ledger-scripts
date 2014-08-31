#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
import argparse

from transaction import Transaction
import db

DEFAULT_ACCOUNT = db.ACCOUNT_CREDIT

parser = argparse.ArgumentParser(description="Import transaction from mobile")
parser.add_argument('--output', help="Output file")
parser.add_argument('file_list', nargs='+', help="File(s) to process")
args = parser.parse_args()

tx = []

for this_file in args.file_list:
    with open(this_file, 'r') as f:
        for line in f:

            cleaned_tx = None

            while cleaned_tx is None:
                t = Transaction()

                split_lines = line.split(" ")

                raw_date = split_lines[0]
                t.valid_transaction_date = datetime.strptime(raw_date, "%m/%d/%y")

                raw_amount = split_lines[1]
                t.amount = Decimal(raw_amount)

                raw_tags = split_lines[2].replace('[', '').replace(']', '').split(',')

                payee = ""

                print line

                while payee == "":
                    payee = raw_input("Payee []: ")
                t.payee = payee

                account_found = False

                t.target_account = DEFAULT_ACCOUNT

                for tag in raw_tags:
                    if tag in db.TARGET_ACCOUNT_MAP:
                        t.target_account = db.TARGET_ACCOUNT_MAP[tag]
                        break

                    if tag in db.SOURCE_ACCOUNT_MAP:
                        t.source_account = db.SOURCE_ACCOUNT_MAP[tag]
                        break

                while t.source_account is None:
                    t.source_account = raw_input("Source account: ")

                t.valid_transaction_date = datetime.strptime(raw_date, "%m/%d/%y")

                print t.to_ledger()

                confirmation = raw_input("Looks good? [y/n/t] ")

                if confirmation[0].capitalize() == "Y":
                    print ""
                    cleaned_tx = t
                elif confirmation[0].capitalize() == "N":
                    print ""
                elif confirmation[0].capitalize() == "T":
                    print "Tagged"
                    t.tagged = True
                    cleaned_tx = t
                else:
                    print "Oops!"

            tx.append(cleaned_tx)

if args.output is not None:
    with open(args.output, 'a') as f:
        for t in tx:
            f.write(t.to_ledger())
else:
    for t in tx:
        print t.to_ledger()