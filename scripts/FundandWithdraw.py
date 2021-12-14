from scripts.helpful_scripts import getaccount
from brownie import FundMe


def fund():
    fund_me = FundMe[-1]
    account = getaccount()
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"The entry fee is {entrance_fee}")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = getaccount()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
