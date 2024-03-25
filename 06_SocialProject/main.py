import sys
import asyncio
from aioconsole import ainput

async def main():
    if len(sys.argv)<3:
        print("Argument error, please use client.py HOST_ADDRESS HOST_PORT")
    else:
        addr = sys.argv[1]
        port = sys.argv[2]

        reader, writer = await asyncio.open_connection(addr, int(port))
        print(f"Connected to {addr}:{port}")

        send = asyncio.create_task(ainput())
        receive = asyncio.create_task(reader.readline())

        msg = ""
        who_is_called = False
        cows_is_called = False
        while msg.strip() != "exit()":
            done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
            for info in done:
                if info is send:
                    send = asyncio.create_task(ainput())
                    msg = info.result()
                    msg += '\n'
                    cmd = msg.split()[0]
                    if cmd == "who":
                        who_is_called = True
                        writer.write(msg.encode())
                        await writer.drain()
                    elif cmd == "say":
                        if who_is_called:
                            writer.write(msg.encode())
                            await writer.drain()
                        else:
                            print("To talk to other users, call \'who\' first")
                    elif cmd == "cows":
                        cows_is_called = True
                        writer.write(msg.encode())
                        await writer.drain()
                    elif cmd == "login":
                        if cows_is_called:
                            cows_is_called = False
                            writer.write(msg.encode())
                            await writer.drain()
                        else:
                            print("To login as an user, call \'cows\' first")
                    else:
                        writer.write(msg.encode())
                        await writer.drain()
                elif info is receive:
                    receive = asyncio.create_task(reader.readline())
                    data = info.result().decode().strip()
                    print(data)
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        sys.exit(1)