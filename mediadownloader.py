import click
import pprint
import telethon
import telethon.sync
from tqdm import tqdm


@click.command()
@click.argument("chat_name")
@click.argument("api_id")
@click.argument("api_hash")
def main(chat_name, api_id, api_hash):
    client = telethon.TelegramClient('session_name', api_id, api_hash).start()
    dialogs = client.get_dialogs()
    try:
        with client.takeout() as takeout:
            for message in tqdm(
                    takeout.iter_messages(
                        chat_name,
                        wait_time=0)):
                try:
                    client.download_media(message)
                except telethon.errors.rpcerrorlist.FloodWaitError as e:
                    print('Must wait', e.seconds, 'to avoid flooding')
                    time.sleep(e.seconds + 2)
                    client.download_media(message)

    except telethon.errors.TakeoutInitDelayError as e:
        print('Must wait', e.seconds, 'before takeout')
        time.sleep(e.seconds)


if __name__ == "__main__":
    main()
