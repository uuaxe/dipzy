# Dipzy

Dipzy is a Python package for interacting with different data and notification/bot APIs.

# Usage

```
import dipzy as dz
from web3 import Web3

# Sending message via Telegram bot 
bot = dz.telegram.Bot(token)
bot.send_message(chat_id, text, parse_mode="MarkdownV2")

# Interacting with the blockchain
w3 = Web3(Web3.HTTPProvider("https://rpc.ankr.com/eth"))
dz.web3.LiquidityPool.set_defaults(w3, erc20_abi)
curve_3pool = dz.web3.CurveLP(address, abi, n=3)
print(curve_3pool)

# Twitter API
twitter = dz.Twitter(bearer_token)
```

# Installation

Install directly from the GitHub repository using pip:

```
pip install git+https://github.com/uuaxe/dipzy.git
```

Alternatively, clone repository from GitHub and install using pip:

```
git clone https://github.com/uuaxe/dipzy.git
cd dipzy
pip install .
```

To install in development mode, replace `pip install .` with:
```
pip install -e .
```

To uninstall:

```
pip uninstall dipzy
```

# API

## web3

The base `LiquidityPool` class has class attributes `w3` and `erc20_abi` which have to be set using the class setter method. These class attributes are inherited by the child class (e.g. `CurveLP`). The `LiquidityPool` inherits from an abstract base class (ABC) and has an abstract method `get_reserves` which has to be implemented by all its child classes. 

## Telegram

- Levels of persistant data: 1) Bot 2) Chat 3) User
- Command handlers are unable to access variables outside of the function
- Command handlers usually take two arguments: update and context
- Error handlers receive the raised TelegramError object in error
- Bot sends message to specified chat IDs

## Twitter

- Twitter supports two authentication methods, OAuth1.0 and OAuth 2.0
- There are two main types of requests:
    1) App-only: Typically GET requests that access public information
    2) User-context: Typically POST requests that perform actions that have to be authenticated by the user
