# My Steam key redeeming script.

Tries to redeem list of keys to my Steam account.  
If redeeming failed with error that I already own the game, then send it with Telegram bot.

## Usage.
1. Install [Python](https://www.python.org).
1. Install [pip](https://pip.pypa.io/en/stable/installation/).
1. Install [required packages](requirements.txt).
   
    `pip install -r requirements.txt`
1. Create [Telegram bot](https://core.telegram.org/bots).
1. Add bot to Telegram channel.
1. Create .env-file.
   - Use [.env.example](.env.example) as base. 
1. Run script with Steam keys as arguments seperated by space.
   
    `python main.py <Steam key> <Steam key 2>`

1. Login to Steam account.
 
## .env-file
| Name               | Description                              |
| ------------------ | ---------------------------------------- |
| TELEGRAM_TOKEN     | Token for Telegram bot.                  |
| TELEGRAM_CHAT_ID   | ID for Telegram chat to send message to. |
| TELEGRAM_MSG_START | Start string for messages.               |


## Example output
```shell
python .\main.py XXXXX-XXXXX-XXXXX XXXXX-XXXXX-XXXXX XXXXX-XXXXX-XXXXX XXXXX-XXXXX-XXXXX
Username: <username>
Password: 
Enter 2FA code: <2FA code>
Key: XXXXX-XXXXX-XXXXX
        Games: ['Valfaris']
        Sent to friend!
Key: XXXXX-XXXXX-XXXXX
        Games: ['Wheels of Aurelia']
        Redeemed!
Key: XXXXX-XXXXX-XXXXX
        Games: ['Wildermyth']
        Redeemed!
Key: XXXXX-XXXXX-XXXXX
        Games: ['XTHRUST']
        Redeemed!
```