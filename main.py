import asyncio
import logging
from aiohttp import web

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UDPProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        """Called when UDP socket is created"""
        self.transport = transport
        logger.info("UDP Server started")

    def datagram_received(self, data, addr):
        """Called when UDP data is received"""
        message = data.decode()
        logger.info(f"Received UDP message from {addr}: {message}")

        # Echo the message back
        response = f"Received UDP: {message}"
        self.transport.sendto(response.encode(), addr)


async def handle_http_request(request):
    """Handle incoming HTTP requests"""
    logger.info(f"Received HTTP {request.method} request from {request.remote}")

    # Return a simple response
    return web.Response(text="Hello from HTTP server!")


async def main():
    # Create event loop
    loop = asyncio.get_event_loop()

    try:
        # Setup HTTP server
        app = web.Application()
        app.router.add_get("/", handle_http_request)  # Handle GET requests
        runner = web.AppRunner(app)
        await runner.setup()
        http_site = web.TCPSite(runner, "0.0.0.0", 8080)
        await http_site.start()
        logger.info("HTTP server started on port 8080")

        # Setup UDP server
        transport, protocol = await loop.create_datagram_endpoint(
            UDPProtocol, local_addr=("fly-global-services", 8080)
        )

        # Keep the servers running
        logger.info("Both servers are now running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(3600)  # Keep alive

    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        # Cleanup
        if "transport" in locals():
            transport.close()
        if "runner" in locals():
            await runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Servers shutting down...")
