import brotli

async def decompress(file_bytes: bytes, file_encoding: str = "utf-8") -> str:
    return str(
        brotli.decompress(file_bytes),
        file_encoding,
    )

