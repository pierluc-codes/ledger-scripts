#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
import argparse

from transaction import Transaction
import transactionui
import db

DEFAULT_ACCOUNT = db.ACCOUNT_CREDIT

parser = argparse.ArgumentParser(description="Import transaction from Visa Desjardins")
parser.add_argument('--output', help="Output file")
parser.add_argument('file_list', nargs='+', help="File(s) to process")
args = parser.parse_args()

tx = []

for this_file in args.file_list:
    with open(this_file, 'r') as f:
        for line in f:

            converted_line = line.decode('iso-8859-1').encode('utf8')

            t = Transaction()

            split_lines = converted_line.split(",")

            raw_date = split_lines[3]
            t.valid_transaction_date = datetime.strptime(raw_date, "%Y/%m/%d")

            raw_debited_amount = split_lines[11].replace("\"", "")
            raw_credited_amount = split_lines[12].replace("\"", "")

            if raw_debited_amount != "":
                t.amount = -Decimal(raw_debited_amount)
            elif raw_credited_amount != "":
                t.amount = Decimal(raw_credited_amount)
            else:
                raise Exception("Transaction without credited or debited amount: " + converted_line)

            t.payee = split_lines[5].replace("\"", "")
            t.tags = None

            tx.append(transactionui.cleanup_tx(DEFAULT_ACCOUNT, t, converted_line, None))

if args.output is not None:
    with open(args.output, 'a') as f:
        for t in tx:
            f.write(t.to_ledger())
else:
    for t in tx:
        print t.to_ledger()