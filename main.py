# Handle .env files.
from dotenv import load_dotenv

# Argument parsing.
import os
from argparse import ArgumentParser

# Redeeming Steam keys.
from steam.client import SteamClient
from steam.enums.common import EResult

# Sending message with Telegram.
from telegram import Bot
from asyncio import run

# Any type.
from typing import Any

async def main():
    """Main function to run asynchronously with asyncio

    Raises:
        Exception: If failed
    """

    # Init argument parser.
    parser: ArgumentParser = ArgumentParser()
    # Add keys as required argument.
    parser.add_argument("keys", nargs="+", help="Steam keys to redeem.")
    # Get keys as string list.
    keys: list[str] = parser.parse_args().keys
    del parser

    # Init Steam client.
    steam_client: SteamClient = SteamClient()

    # Login to Steam client.
    steam_client.cli_login()
    # Try to run with steam client.
    try:
        # Load .env file.
        load_dotenv(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env"))

        # Init Telegram bot.
        telegram_bot: Bot = Bot(os.getenv("TELEGRAM_TOKEN"))
        TELEGRAM_CHAT_ID: str|None = os.getenv("TELEGRAM_CHAT_ID")
        TELEGRAM_MSG_START: str|None = os.getenv("TELEGRAM_MSG_START")

        # Loop keys from arguments.
        for key in keys:
            # Print current key.
            print("Key:", key)

            # Try to redeem key.
            eresult: EResult
            result_details: Any|None
            receipt_info: Any|None
            eresult, result_details, receipt_info = steam_client.register_product_key(key)

            # Has game already?
            has_already: bool = eresult == EResult.Fail and result_details == 9

            # If did not has already and did not success.
            if not has_already and eresult != EResult.OK:
                # If result was failure.
                if eresult == EResult.Fail:
                    # If resutl details is 53.
                    if result_details == 53:
                        # Inform that there where too many recent activation attemps.
                        raise Exception("Too many recent activation attempts!")
                # Raise exception with error data.
                raise Exception("Code redeem failed!", eresult, result_details, receipt_info)
            del eresult
            del result_details

            # Init game names.
            game_names: list[str] = []
            # Add game names from line items.
            for _, lineItem in receipt_info["lineitems"].items():
                game_names.append(lineItem["ItemDescription"])
            del receipt_info

            # Print game names.
            print("\tGames:", game_names)

            # Has game already.
            if has_already:
                # Send key to friend.
                async with telegram_bot:
                    await telegram_bot.send_message(
                        TELEGRAM_CHAT_ID,
                        TELEGRAM_MSG_START + " " + ", ".join(game_names) + ": " + key,
                        parse_mode="Markdown",
                    )
                    print("\tSent to friend!")
            # Key was redeemed.
            else:
                print("\tRedeemed!")
            del key
            del has_already
            del game_names
        del keys
        del telegram_bot
        del TELEGRAM_CHAT_ID
        del TELEGRAM_MSG_START
    # Finally.
    finally:
        # Logout from Steam.
        steam_client.logout()
        del steam_client

    # Exit with success.
    exit(0)

# Run main function asynchronously with asyncio. 
if __name__ == '__main__':
    run(main())
