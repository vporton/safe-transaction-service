import json
from logging import getLogger
from typing import Any, Dict, List, Tuple, Union, cast

from eth_utils import function_abi_to_4byte_selector
from hexbytes import HexBytes
from web3 import Web3
from web3._utils.abi import (get_abi_input_names, get_abi_input_types,
                             map_abi_data)
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract import Contract, ContractFunction

from gnosis.eth.contracts import (get_safe_contract, get_safe_V0_0_1_contract,
                                  get_safe_V1_0_0_contract)

logger = getLogger(__name__)


AbiType = Dict[str, Any]


conditional_token_abi = json.loads('[{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"},{"name":"","type":"uint256"}],"name":"payoutNumerators","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"ids","type":"uint256[]"},{"name":"values","type":"uint256[]"},{"name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"owners","type":"address[]"},{"name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"operator","type":"address"},{"name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"payoutDenominator","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"from","type":"address"},{"name":"to","type":"address"},{"name":"id","type":"uint256"},{"name":"value","type":"uint256"},{"name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"conditionId","type":"bytes32"},{"indexed":true,"name":"oracle","type":"address"},{"indexed":true,"name":"questionId","type":"bytes32"},{"indexed":false,"name":"outcomeSlotCount","type":"uint256"}],"name":"ConditionPreparation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"conditionId","type":"bytes32"},{"indexed":true,"name":"oracle","type":"address"},{"indexed":true,"name":"questionId","type":"bytes32"},{"indexed":false,"name":"outcomeSlotCount","type":"uint256"},{"indexed":false,"name":"payoutNumerators","type":"uint256[]"}],"name":"ConditionResolution","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"stakeholder","type":"address"},{"indexed":false,"name":"collateralToken","type":"address"},{"indexed":true,"name":"parentCollectionId","type":"bytes32"},{"indexed":true,"name":"conditionId","type":"bytes32"},{"indexed":false,"name":"partition","type":"uint256[]"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"PositionSplit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"stakeholder","type":"address"},{"indexed":false,"name":"collateralToken","type":"address"},{"indexed":true,"name":"parentCollectionId","type":"bytes32"},{"indexed":true,"name":"conditionId","type":"bytes32"},{"indexed":false,"name":"partition","type":"uint256[]"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"PositionsMerge","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"redeemer","type":"address"},{"indexed":true,"name":"collateralToken","type":"address"},{"indexed":true,"name":"parentCollectionId","type":"bytes32"},{"indexed":false,"name":"conditionId","type":"bytes32"},{"indexed":false,"name":"indexSets","type":"uint256[]"},{"indexed":false,"name":"payout","type":"uint256"}],"name":"PayoutRedemption","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"operator","type":"address"},{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"id","type":"uint256"},{"indexed":false,"name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"operator","type":"address"},{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"ids","type":"uint256[]"},{"indexed":false,"name":"values","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"operator","type":"address"},{"indexed":false,"name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"value","type":"string"},{"indexed":true,"name":"id","type":"uint256"}],"name":"URI","type":"event"},{"constant":false,"inputs":[{"name":"oracle","type":"address"},{"name":"questionId","type":"bytes32"},{"name":"outcomeSlotCount","type":"uint256"}],"name":"prepareCondition","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"questionId","type":"bytes32"},{"name":"payouts","type":"uint256[]"}],"name":"reportPayouts","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"collateralToken","type":"address"},{"name":"parentCollectionId","type":"bytes32"},{"name":"conditionId","type":"bytes32"},{"name":"partition","type":"uint256[]"},{"name":"amount","type":"uint256"}],"name":"splitPosition","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"collateralToken","type":"address"},{"name":"parentCollectionId","type":"bytes32"},{"name":"conditionId","type":"bytes32"},{"name":"partition","type":"uint256[]"},{"name":"amount","type":"uint256"}],"name":"mergePositions","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"collateralToken","type":"address"},{"name":"parentCollectionId","type":"bytes32"},{"name":"conditionId","type":"bytes32"},{"name":"indexSets","type":"uint256[]"}],"name":"redeemPositions","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"conditionId","type":"bytes32"}],"name":"getOutcomeSlotCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"oracle","type":"address"},{"name":"questionId","type":"bytes32"},{"name":"outcomeSlotCount","type":"uint256"}],"name":"getConditionId","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"parentCollectionId","type":"bytes32"},{"name":"conditionId","type":"bytes32"},{"name":"indexSet","type":"uint256"}],"name":"getCollectionId","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"collateralToken","type":"address"},{"name":"collectionId","type":"bytes32"}],"name":"getPositionId","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"}]')
market_maker_abi = json.loads('[{"constant":true,"inputs":[{"name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"resume","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"pmSystem","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"outcomeTokenAmounts","type":"int256[]"},{"name":"collateralLimit","type":"int256"}],"name":"trade","outputs":[{"name":"netCost","type":"int256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"close","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"withdrawFees","outputs":[{"name":"fees","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"fundingChange","type":"int256"}],"name":"changeFunding","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"isOwner","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"whitelist","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"outcomeTokenCost","type":"uint256"}],"name":"calcMarketFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"collateralToken","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_operator","type":"address"},{"name":"","type":"address"},{"name":"","type":"uint256[]"},{"name":"","type":"uint256[]"},{"name":"","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"stage","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"funding","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"conditionIds","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"atomicOutcomeSlotCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"fee","outputs":[{"name":"","type":"uint64"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_fee","type":"uint64"}],"name":"changeFee","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"operator","type":"address"},{"name":"","type":"address"},{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"bytes"}],"name":"onERC1155Received","outputs":[{"name":"","type":"bytes4"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"FEE_RANGE","outputs":[{"name":"","type":"uint64"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"initialFunding","type":"uint256"}],"name":"AMMCreated","type":"event"},{"anonymous":false,"inputs":[],"name":"AMMPaused","type":"event"},{"anonymous":false,"inputs":[],"name":"AMMResumed","type":"event"},{"anonymous":false,"inputs":[],"name":"AMMClosed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"fundingChange","type":"int256"}],"name":"AMMFundingChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"newFee","type":"uint64"}],"name":"AMMFeeChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"fees","type":"uint256"}],"name":"AMMFeeWithdrawal","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"transactor","type":"address"},{"indexed":false,"name":"outcomeTokenAmounts","type":"int256[]"},{"indexed":false,"name":"outcomeTokenNetCost","type":"int256"},{"indexed":false,"name":"marketFees","type":"uint256"}],"name":"AMMOutcomeTokenTrade","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"constant":true,"inputs":[{"name":"outcomeTokenAmounts","type":"int256[]"}],"name":"calcNetCost","outputs":[{"name":"netCost","type":"int256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"outcomeTokenIndex","type":"uint8"}],"name":"calcMarginalPrice","outputs":[{"name":"price","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
market_maker_factory_abi = json.loads('[{"constant":true,"inputs":[],"name":"implementationMaster","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"creator","type":"address"},{"indexed":false,"name":"lmsrMarketMaker","type":"address"},{"indexed":false,"name":"pmSystem","type":"address"},{"indexed":false,"name":"collateralToken","type":"address"},{"indexed":false,"name":"conditionIds","type":"bytes32[]"},{"indexed":false,"name":"fee","type":"uint64"},{"indexed":false,"name":"funding","type":"uint256"}],"name":"LMSRMarketMakerCreation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"initialFunding","type":"uint256"}],"name":"AMMCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"target","type":"address"},{"indexed":false,"name":"clone","type":"address"}],"name":"CloneCreated","type":"event"},{"constant":false,"inputs":[{"name":"consData","type":"bytes"}],"name":"cloneConstructor","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"pmSystem","type":"address"},{"name":"collateralToken","type":"address"},{"name":"conditionIds","type":"bytes32[]"},{"name":"fee","type":"uint64"},{"name":"whitelist","type":"address"},{"name":"funding","type":"uint256"}],"name":"createLMSRMarketMaker","outputs":[{"name":"lmsrMarketMaker","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')


class TxDecoderException(Exception):
    pass


class UnexpectedProblemDecoding(TxDecoderException):
    pass


class CannotDecode(TxDecoderException):
    pass


def get_tx_decoder() -> 'TxDecoder':
    if not hasattr(get_tx_decoder, 'instance'):
        get_tx_decoder.instance = TxDecoder()
    return get_tx_decoder.instance


class TxDecoder:
    """
    Decode txs for supported contracts
    """
    def __init__(self):
        self.dummy_w3 = Web3()
        sight_contracts = [self.dummy_w3.eth.contract(abi=abi) for abi in (conditional_token_abi,
                                                                           market_maker_abi,
                                                                           market_maker_factory_abi)]

        # Order is important. If signature is the same (e.g. renaming of `baseGas`) last elements in the list
        # will take preference
        self.supported_contracts = sight_contracts + [get_safe_V0_0_1_contract(self.dummy_w3),
                                                      get_safe_V1_0_0_contract(self.dummy_w3),
                                                      get_safe_contract(self.dummy_w3)]

        # Web3 generates possible selectors every time. We cache that and use a dict to do a fast check
        # Store selectors with abi
        self.supported_fn_selectors: Dict[bytes, ContractFunction] = {}
        for supported_contract in self.supported_contracts:
            self.supported_fn_selectors.update(self._generate_selectors_with_abis_from_contract(supported_contract))

    def _generate_selectors_with_abis_from_contract(self, contract: Contract) -> Dict[bytes, ContractFunction]:
        return {function_abi_to_4byte_selector(contract_fn.abi): contract_fn
                for contract_fn in contract.all_functions()}

    def _parse_decoded_arguments(self, decoded_value: Any) -> Any:
        """
        Parse decoded arguments, like converting `bytes` to hexadecimal `str`
        :param decoded:
        :return: Dict[str, Any]
        """
        if isinstance(decoded_value, bytes):
            decoded_value = HexBytes(decoded_value).hex()
        return decoded_value

    def decode_transaction_with_types(self, data: Union[bytes, str]) -> Tuple[str, List[Tuple[str, str, Any]]]:
        """
        Decode tx data
        :param data: Tx data as `hex string` or `bytes`
        :return: Tuple with the `function name` and a list of dictionaries dictionary {'name', 'type', 'value'}
        :raises: CannotDecode if data cannot be decoded. You should catch this exception when using this function
        :raises: UnexpectedProblemDecoding if there's an unexpected problem decoding (it shouldn't happen)
        """
        fn_name, parameters = self._decode_transaction(data)
        return fn_name, [{'name': name, 'type': argument_type, 'value': value}
                         for name, argument_type, value in parameters]

    def decode_transaction(self, data: Union[bytes, str]) -> Tuple[str, Dict[str, Any]]:
        """
        Decode tx data
        :param data: Tx data as `hex string` or `bytes`
        :return: Tuple with the `function name` and a dictionary with the arguments of the function
        :raises: CannotDecode if data cannot be decoded. You should catch this exception when using this function
        :raises: UnexpectedProblemDecoding if there's an unexpected problem decoding (it shouldn't happen)
        """
        fn_name, parameters = self._decode_transaction(data)
        return fn_name, {name: value for name, argument_type, value in parameters}

    def _decode_transaction(self, data: Union[bytes, str]) -> Tuple[str, List[Tuple[str, str, Any]]]:
        """
        Decode tx data
        :param data: Tx data as `hex string` or `bytes`
        :return: Tuple with the `function name` and a List of sorted tuples with
        the `name` of the argument, `type` and `value`
        :raises: CannotDecode if data cannot be decoded. You should catch this exception when using this function
        :raises: UnexpectedProblemDecoding if there's an unexpected problem decoding (it shouldn't happen)
        """

        if not data:
            raise CannotDecode(data)

        data = HexBytes(data)
        selector, params = data[:4], data[4:]
        if selector not in self.supported_fn_selectors:
            raise CannotDecode(data.hex())

        try:
            contract_fn = self.supported_fn_selectors[selector]
            names = get_abi_input_names(contract_fn.abi)
            types = get_abi_input_types(contract_fn.abi)
            decoded = self.dummy_w3.codec.decode_abi(types, cast(HexBytes, params))
            normalized = map_abi_data(BASE_RETURN_NORMALIZERS, types, decoded)
            values = map(self._parse_decoded_arguments, normalized)
        except ValueError as exc:
            raise UnexpectedProblemDecoding from exc

        return contract_fn.fn_name, list(zip(names, types, values))
