from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    getaccount,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fundme():
    account = getaccount()
    # pass the price feed address to our FundMe contract.
    # If we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"  # the network.show_active() here will show us which network we are on, and by doing so it will get the
            # price feed from our brownie-config.yaml code, since this is the layout we are using to store the price feeds/addresses.
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fundme()