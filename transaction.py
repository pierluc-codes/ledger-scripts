class Transaction:

    def __init__(self):
        self.valid_transaction_date = None
        self.payee = None
        self.target_account = None
        self.source_account = None
        self.amount = None
        self.tagged = False

        pass

    TEMPLATE = (
        "%(tx_date)s %(payee)s\n"
        "\t%(target_account)s\t$%(amount)s\n"
        "\t%(source_account)s\n\n"
    )

    TAGGED_TEMPLATE = (
        "; *********************\n"
        "%(tx_date)s %(payee)s\n"
        "\t%(target_account)s\t$%(amount)s\n"
        "\t%(source_account)s\n"
        "; *********************\n\n"
    )

    def to_ledger(self):

        if self.tagged:
            base_string = Transaction.TAGGED_TEMPLATE
        else:
            base_string = Transaction.TEMPLATE

        return base_string % {
            "tx_date": self.valid_transaction_date.strftime("%Y/%m/%d"),
            "payee": self.payee,
            "target_account": self.target_account,
            "source_account": self.source_account,
            "amount": "%.2f" % self.amount,
        }

