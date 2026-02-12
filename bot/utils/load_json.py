import aiofiles
import json

async def load_json(filepath: str) -> dict:
    try:
        async with aiofiles.open(file=filepath, mode='r') as f:
            content = await f.read()

        data = json.loads(content)
        return data
    except FileNotFoundError:
        print(f"Error: {filepath} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Error: could not read json from the file: {filepath}")
        return {}
