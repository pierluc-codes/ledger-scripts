#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transaction import Transaction

import db


def cleanup_tx(default_account, partial_transaction, line, tags):
    cleaned_tx = None

    while cleaned_tx is None:
        t = Transaction()

        print line

        t.payee = partial_transaction.payee

        while t.payee == "":
            t.payee = raw_input("Payee []: ")

        if t.payee in db.PAYEE_SOURCE_ACCOUNT_MAP:
            t.source_account = db.PAYEE_SOURCE_ACCOUNT_MAP[t.payee]

        t.target_account = default_account

        if tags is not None:
            for tag in tags:
                if tag in db.TARGET_ACCOUNT_MAP:
                    t.target_account = db.TARGET_ACCOUNT_MAP[tag]
                    break

                if tag in db.SOURCE_ACCOUNT_MAP:
                    t.source_account = db.SOURCE_ACCOUNT_MAP[tag]
                    break

        while t.source_account is None:
            t.source_account = raw_input("Source account: ")

        t.valid_transaction_date = partial_transaction.valid_transaction_date

        if partial_transaction.amount < 0:
            original_source_account = t.source_account

            t.source_account = t.target_account
            t.target_account = original_source_account

        t.amount = abs(partial_transaction.amount)

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

    return cleaned_tx