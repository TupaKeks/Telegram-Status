import asyncio
import signal
import sys
import time

from telethon import TelegramClient, errors
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest

from spotify_info import main
from spotify_info import main_access_token, get_refresh

api_id = None
api_hash = 'hash'
client = TelegramClient('anon', api_id, api_hash)

about = ""  # default value


async def wait_until(condition):
    while not condition():
        await asyncio.sleep(1)


async def start():
    try:
        access_token = main_access_token()
        password = ""  # if you have two-factor authentication fill this line with your password
        await client.start(password=password)

        expires_at = 3600

        me = await client.get_me()
        print(me.stringify())

        username = me.username
        print(username)
        print(me.phone)

        full = await client(GetFullUserRequest(username))
        bio = full.full_user.about
        print(bio)

        current_track_id = None
        current_description = about

        while True:
            try:
                current_track_info = main(access_token, current_track_id)
                status = current_track_info['is_playing']
                current_time = time.time()

                if status:
                    artists_list = current_track_info['artists'].split(', ')
                    first_artist = artists_list[0]
                    new_description = f"Listens to: {current_track_info['track_name']} - {first_artist}"

                    # Проверяем, изменилось ли описание
                    if new_description != current_description:
                        await client(UpdateProfileRequest(about=new_description))
                        current_description = new_description
                        await asyncio.sleep(5)
                else:
                    # Проверяем, изменилось ли описание
                    if current_description != about:
                        await client(UpdateProfileRequest(about=about))
                        current_description = about
                        await asyncio.sleep(5)

                if current_time - expires_at < 10:
                    access_token = get_refresh()
                    current_time = time.time()
                    continue

                await asyncio.sleep(5)
            except Exception as e:
                if isinstance(e, errors.FloodWaitError):
                    print(e)
                    await asyncio.sleep(e.seconds)
                    continue
                elif e == "Expecting value: line 1 column 1 (char 0)":
                    continue
                else:
                    print(e)

    except Exception as e:
        print(e)


async def loop():
    try:
        await start()
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Updating profile bio...")
        await client(UpdateProfileRequest(about=about))
        sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)
    asyncio.run(loop())
