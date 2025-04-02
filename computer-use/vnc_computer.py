import base64
import io
import time
import asyncvnc

class VNCComputer:
    """Controls a remote computer using VNC."""

    def __init__(self, host, port=5900, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.dimensions = (0, 0)
        self.environment = "unknown"

    async def connect(self):
        self.client = await asyncvnc.connect(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password
        )
        self.dimensions = await self.client.get_screen_size()
        self.environment = "remote"

    async def screenshot(self) -> str:
        screenshot = await self.client.screenshot()
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)
        data = bytearray(buffer.getvalue())
        return base64.b64encode(data).decode("utf-8")

    async def click(self, x: int, y: int, button: str = "left") -> None:
        await self.client.click(x, y, button=button)

    async def double_click(self, x: int, y: int) -> None:
        await self.client.double_click(x, y)

    async def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
        await self.client.scroll(x, y, scroll_x, scroll_y)

    async def type(self, text: str) -> None:
        await self.client.type(text)

    async def wait(self, ms: int = 1000) -> None:
        time.sleep(ms / 1000)

    async def move(self, x: int, y: int) -> None:
        await self.client.move(x, y)

    async def keypress(self, keys: list[str]) -> None:
        await self.client.keypress(keys)

    async def drag(self, path: list[dict[str, int]]) -> None:
        await self.client.drag(path)
