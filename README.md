# Dipzy

Dipzy is a Python package for interacting with different data and notification/bot APIs.

# Usage

```
import dipzy as dz

twitter = dz.Twitter(bearer_token)
dict = dz.utils.filter_dict(dict, keys)
```

# Supported APIs

## Telegram

- Levels of persistant data: 1) Bot 2) Chat 3) User
- Command handlers are unable to access variables outside of the function
- Command hanlders usually take two arguments: update and context
- Error handlers receive the raised TelegramError object in error
- Bot sends message to specified chat IDs

## Twitter

- Twitter supports two authentication methods, OAuth1.0 and OAuth 2.0
- There are two main types of requests:
    1) App-only: Typically GET requests that access public information
    2) User-context: Typically POST requests that perform actions that have to be authenticated by the user