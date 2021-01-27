import math


class Category:
    def __init__(self, name) -> None:
        self.name = name
        self.ledger = list()

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.name)
            category.deposit(amount, "Transfer from " + self.name)
            return True
        else:
            return False

    def __str__(self):
        buffer_length = (30 - len(self.name)) // 2
        to_string = '*' * buffer_length + self.name + '*' * buffer_length+'\n'
        for item in self.ledger:
            to_string += "{:<23}{:>7.2f}\n".format(item["description"][0:min(23, len(item["description"]))], item["amount"])
        to_string += "Total: "+str(self.get_balance())
        return to_string


def create_spend_chart(categories):
    if len(categories) == 0:
        pass
    else:
        withdrawal_list = list()
        withdrawal_total_overall = 0.0
        for category in categories:
            withdrawal_total_per_category = 0.0
            for item in category.ledger:
                if item["amount"] < 0.0:
                    withdrawal_total_per_category += -item["amount"]
            withdrawal_list.append(withdrawal_total_per_category)
            withdrawal_total_overall += withdrawal_total_per_category
        withdrawal_percentage = list()
        for i in range(len(withdrawal_list)):
            withdrawal_percentage.append(math.floor(withdrawal_list[i]/withdrawal_total_overall*10)*10)
    spend_chart = "Percentage spent by category\n"
    for percentage_tick in range(100, -1, -10):
        spend_chart += "{:>3}| ".format( str(percentage_tick))
        for i in range(len(withdrawal_percentage)):
            spend_chart += "{}  ".format("o" if withdrawal_percentage[i] >= percentage_tick else " ")
        spend_chart += "\n"
    spend_chart += "    "+len(withdrawal_percentage)*"---"+"-\n"
    max_length=None
    for i in range(len(categories)):
        if max_length is None or max_length < len(categories[i].name):
            max_length = len(categories[i].name)
    for i in range(max_length):
        spend_chart += "     "
        for j in range(len(categories)):
            spend_chart += (categories[j].name[i] if len(categories[j].name)>i else " ")+"  "
        if i != max_length-1:
            spend_chart += "\n"
    return spend_chart
