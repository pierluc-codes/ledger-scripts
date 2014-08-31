#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import date
from decimal import Decimal, InvalidOperation


def ask(arg, message):
    if arg is not None:
        return arg
    else:
        result = ""
        while result == "":
            result = raw_input(message)
        return result


parser = argparse.ArgumentParser(description="Generate ledger transaction.")

parser.add_argument("--date", help="Specifies date of the transaction")
parser.add_argument("--payee", help="Specifies payee of the transaction")
parser.add_argument("--target", help="Specifies target account of the transaction")
parser.add_argument("--source", help="Specifies source account of the transaction")
parser.add_argument("--amount", help="Specifies amount of the transaction")

args = parser.parse_args()

if args.date is not None:
    transaction_date = args.date

valid_transaction_date = None

while valid_transaction_date is None:
    try:
        transaction_date = raw_input("No date specified. Please specifies a date [today]: ")

        if transaction_date == "":
            valid_transaction_date = date.today()
        else:
            valid_transaction_date = date.strptime(transaction_date, "%Y/%m/%d")
    except ValueError, e:
        print "Invalid date. Please enter a valid date: "

payee = ask(args.payee, "No payee specified. Please specifies a payee []: ")

if args.amount is not None:
    amount = args.amount
else:
    amount = ""
    while amount == "":
        amount = raw_input("No amount specified. Please enter an amount: ")
        try:
            amount = Decimal(amount)
        except InvalidOperation, e:
            print "Invalid amount. Please entry a decimal value"
            amount = ""

target_account = ask(args.target, "No target account specified. Please specifies an account []:")
source_account = ask(args.source, "No source account specified. Please specifies an account []:")

base = (
    "%(tx_date)s %(payee)s\n"
    "\t%(target_account)s\t$%(amount)s\n"
    "\t%(source_account)s\n"
)

print base % {
    "tx_date": valid_transaction_date,
    "payee": payee,
    "target_account": target_account,
    "source_account": source_account,
    "amount": amount,
}

