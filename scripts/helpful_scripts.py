from brownie import (
    VRFCoordinatorMock,
    MockV3Aggregator, 
    LinkToken,
    Contract, 
    accounts, 
    network,
    config
)


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"] # mainnet-fork-dev
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or \
       network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])
                                                                                                                                                                                                                                                                                                                                                                                        

contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator,
                    "vfr_coordinator": VRFCoordinatorMock,
                    "link_token": LinkToken}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 2000_0000_0000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed!")
