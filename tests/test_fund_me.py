from brownie.network import account
from scripts.helpful_scripts import getaccount, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fundme
from brownie import network, accounts, exceptions
import pytest


def testFundAndWithdraw():
    account = getaccount()
    fund_me = deploy_fundme()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for Local Testing")
    account = getaccount()
    fund_me = deploy_fundme()
    bad_actor = accounts.add()
    with pytest.raises(
        exceptions.VirtualMachineError
    ):  # here we are saying, pytest we want this to raise an error, so instead of showing
        # failed, we would want it to show passed, that the error WAS passed that only the owner can withdraw.
        fund_me.withdraw({"from": bad_actor})
