import abc
import enum
from dataclasses import dataclass


class Address(enum.Enum):
    ETH = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"


@dataclass
class Reserve:
    '''Individual reserve in a liquidity pool'''
    symbol: str
    decimals: int
    balance: int


class LiquidityPool(abc.ABC):
    '''
    Abstract class for liquidity pool. Implement method get_reserves.
    
    Args:
        address (str): Contract address
        abi (list | dict): Contract ABI
        n (int): Number of reserves
    '''
    
    # Set class attributes using class method: set_defaults
    w3 = None
    erc20_abi = None
    
    @classmethod
    def set_defaults(cls, w3, erc20_abi):
        cls.w3 = w3
        cls.erc20_abi = erc20_abi
    
    def __init__(self, address, abi, n):
        # Set class attributes before instantiating LiquidityPool!
        assert self.w3 is not None and self.erc20_abi is not None

        self.address = address
        self.abi = abi
        self.n = n
        self.contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(address),
            abi=abi
        )
        self.token_addresses = None
        self.reserves = {}

        self.get_reserves()
    
    @abc.abstractmethod
    def get_reserves():
        pass 
            
    def __str__(self):
        assert len(self.reserves) > 0
        balances = [
            f"{reserve.balance / 10 ** (reserve.decimals):,.0f} {symbol}"
            for symbol, reserve in self.reserves.items()
        ]
        return "\n".join(balances)


class CurveLP(LiquidityPool):
    def get_reserves(self):
        self.token_addresses = [
            self.contract.functions.coins(i).call() for i in range(self.n)
        ]
        for i, addr in enumerate(self.token_addresses):
            if addr == Address.ETH.value:
                balance = self.contract.functions.balances(i).call()
                self.reserves["ETH"] = Reserve("ETH", 18, balance)
            else:
                token = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(addr),
                    abi=self.erc20_abi
                )
                symbol = token.functions.symbol().call()
                self.reserves[symbol] = Reserve( 
                    symbol,
                    token.functions.decimals().call(),
                    self.contract.functions.balances(i).call()
                )


class UniswapV3LP(LiquidityPool):
    def get_reserves(self):
        self.token_addresses = [
            self.contract.functions.token0().call(),
            self.contract.functions.token1().call()
        ]
        for addr in self.token_addresses:
            token = self.w3.eth.contract(
                address=self.w3.to_checksum_address(addr),
                abi=self.erc20_abi
            )
            symbol = token.functions.symbol().call()
            self.reserves[symbol] = Reserve( 
                symbol,
                token.functions.decimals().call(),
                token.functions.balanceOf(self.address).call()
            )
