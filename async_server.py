import asyncio
from http import HttpServer  # Sesuaikan dengan struktur proyek Anda

httpserver = HttpServer()

async def handle_client(reader, writer):
    global rcv
    rcv = ""
    while True:
        data = await reader.read(1024)
        if not data:
            break
        rcv += data.decode()
        if rcv.endswith('\r\n\r\n'):
            hasil = httpserver.proses(rcv)
            writer.write(hasil)
            await writer.drain()
            rcv = ""
            writer.close()

async def main():
    portnumber = 60001  # Pastikan portnya benar
    server = await asyncio.start_server(
        handle_client, '0.0.0.0', portnumber)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
