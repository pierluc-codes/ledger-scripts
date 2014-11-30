#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
import argparse

from transaction import Transaction
import transactionui
import db

DEFAULT_ACCOUNT = db.ACCOUNT_CASH

parser = argparse.ArgumentParser(description="Import transaction from mobile")
parser.add_argument('--output', help="Output file")
parser.add_argument('file_list', nargs='+', help="File(s) to process")
args = parser.parse_args()

tx = []

for this_file in args.file_list:
    with open(this_file, 'r') as f:
        for line in f:

            t = Transaction()

            split_lines = line.split(" ")

            raw_date = split_lines[0]
            t.valid_transaction_date = datetime.strptime(raw_date, "%d/%m/%Y")

            raw_amount = split_lines[1]
            t.amount = Decimal(raw_amount)

            raw_tags = split_lines[2].replace('[', '').replace(']', '').split(',')

            t.payee = ""

            tx.append(transactionui.cleanup_tx(DEFAULT_ACCOUNT, t, line, raw_tags))

if args.output is not None:
    with open(args.output, 'a') as f:
        for t in tx:
            f.write(t.to_ledger())
else:
    for t in tx:
        print t.to_ledger()
