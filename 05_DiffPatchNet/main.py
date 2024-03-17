import asyncio
import cowsay as cs

clients = {}
logins = {}

async def handle_client(reader, writer):
    addr = "{}:{}".format(*writer.get_extra_info('peername'))
    clients[addr] = asyncio.Queue()
    print(f"{addr} Connected")
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[addr].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for info in done:
            if info is send:
                send = asyncio.create_task(reader.readline())
                message = info.result().decode().strip()
                cmd, *message = message.split(' ')
                message = ' '.join(message)
                if cmd == 'who':
                    await clients[addr].put(f"{list(logins.values())}")
                elif cmd == 'cows':
                    list_usr = list(logins.values())
                    list_cow = cs.list_cows()
                    await clients[addr].put(f"{list(set(list_cow)-set(list_usr))}")
                elif cmd == 'login':
                    if addr in logins.keys():
                        await clients[addr].put(f"Hello {logins[addr]}, you already logged in")
                    elif message.strip() in cs.list_cows():
                        if message.strip() in logins.values():
                            await clients[addr].put(f"login {message.strip()} is not a avalable")
                        else:
                            logins[addr] = message.strip()
                    else:
                        await clients[addr].put(f"{message.strip()} is not a useable login")
                elif cmd == 'say':
                    if addr in logins.keys():
                        login, *message = message.split(' ')
                        message = ' '.join(message)
                        for ip, val in logins.items():
                            if val == login:
                                await clients[ip].put(f"{cs.cowsay(message.strip(), cow = logins[addr])}")
                    else:
                        await clients[addr].put(f"Please login first, call login")
                elif cmd == 'yield':
                    if addr in logins.keys():
                        for out in clients.values():
                            if out is not clients[addr]:
                                await out.put(f"{cs.cowsay(message.strip(), cow = logins[addr])}")
                    else:
                        await clients[addr].put(f"Please login first, call login")
                elif cmd == 'quit':
                    if addr in logins.keys():
                        del logins[addr]
                    else:
                        await clients[addr].put(f"You are not logged in, please login first")
                else:
                    msg = "who - view registered users " 
                    + "\ncows - view available cow names" 
                    + "\nlogin cow_name - register under the name cow_name"
                    + "\nsay cow_name message_text - send a message to the user cow_name"
                    + "\nyield message text - send a message to all registered users"
                    + "\nquit - logout"
                    await clients[addr].put(msg)
            elif info is receive:
                receive = asyncio.create_task(clients[addr].get())
                writer.write(f"{info.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(addr, "DONE")
    del clients[addr]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    print(f'Service started')
    async with server:
        await server.serve_forever()

asyncio.run(main())
