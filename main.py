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
        TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_CHAT_ID")
        TELEGRAM_MSG_START: str | None = os.getenv("TELEGRAM_MSG_START")

        # Dictonary keys.
        KEY_LINEITEMS: str = "lineitems"
        KEY_ITEM_DESCRIPTION: str = "ItemDescription"

        # Loop keys from arguments.
        for key in keys:
            # Print current key.
            print("Key:", key)

            # Try to redeem key.
            eresult: EResult
            result_details: Any | None
            receipt_info: Any | None
            eresult, result_details, receipt_info = steam_client.register_product_key(
                key
            )

            # Init game names.
            game_names: list[str] = []
            # If receipt_info is dictonary and KEY_LINEITEMS is one of it's keys.
            if isinstance(receipt_info, dict) and KEY_LINEITEMS in receipt_info:
                # Get lineitems.
                lineitems = receipt_info[KEY_LINEITEMS]
                # If lineitems is dictonary.
                if isinstance(lineitems, dict):
                    # Loop it's items.
                    for lineItemKey, lineItem in receipt_info[KEY_LINEITEMS].items():
                        # Delete key.
                        del lineItemKey
                        # If line item is dictonary and KEY_ITEM_DESCRIPTION is one of it's keys.
                        if (
                            isinstance(lineItem, dict)
                            and KEY_ITEM_DESCRIPTION in lineItem
                        ):
                            # Get item description.
                            item_description = lineItem[KEY_ITEM_DESCRIPTION]
                            # If item description is string.
                            if isinstance(item_description, str):
                                # Append it to game names.
                                game_names.append(item_description)
                            del item_description
                        del lineItem
                    # If has game names.
                    if game_names:
                        # Print game names.
                        print("\tGames:", game_names)
                del lineitems

            # If key was redeemed.
            if eresult == EResult.OK:
                # Print it out.
                print("\tRedeemed!")
            # If result was failure.
            elif eresult == EResult.Fail:
                # If result details is 9, meaning that you already have this item.
                if result_details == 9:
                    # Send key to friend.
                    async with telegram_bot:
                        await telegram_bot.send_message(
                            TELEGRAM_CHAT_ID,
                            TELEGRAM_MSG_START
                            + " "
                            + ", ".join(game_names)
                            + ": "
                            + key,
                            parse_mode="Markdown",
                        )
                        print("\tSent to friend!")
                # If result details is 24.
                elif result_details == 24:
                    # Inform that code requires ownership of another product.
                    print("\tRequires ownership of another product!")
                # If result details is 53.
                elif result_details == 53:
                    # Inform that there where too many recent activation attemps.
                    raise Exception("\tToo many recent activation attempts!")
                else:
                    # Raise exception with error data.
                    raise Exception(
                        "Code redeem failed!", eresult, result_details, receipt_info
                    )
            else:
                # Raise exception with error data.
                raise Exception(
                    "Code redeem did not return success or fail!",
                    eresult,
                    result_details,
                    receipt_info,
                )
            del key, eresult, result_details, game_names
        del (
            telegram_bot,
            TELEGRAM_CHAT_ID,
            TELEGRAM_MSG_START,
            KEY_LINEITEMS,
            KEY_ITEM_DESCRIPTION,
        )
    # Finally.
    finally:
        # Logout from Steam.
        steam_client.logout()
        del steam_client
    del keys

    # Exit with success.
    exit(0)


# Run main function asynchronously with asyncio.
if __name__ == "__main__":
    run(main())
