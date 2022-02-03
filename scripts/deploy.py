from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


# with the __init__.py file, python knows it can import from othe scripts and packages in project.

# with the above we importing the get_account function from helpful_scripts


def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # making a state change so must put in the from account
    print(f"Contract deployed to {fund_me.address}")
    return fund_me  # so that our tests can have this fund me contract to work with.


def main():
    deploy_fund_me()
