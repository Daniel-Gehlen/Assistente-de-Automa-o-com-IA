import asyncio
import aiohttp

API_BASE = "http://localhost:8000"

async def example_health_check():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE}/health") as resp:
            data = await resp.json()
            print("Health:", data)

async def example_process_task():
    async with aiohttp.ClientSession() as session:
        payload = {
            "task": "Crie uma função Python",
            "agent_name": "coding_assistant"
        }
        async with session.post(f"{API_BASE}/api/agents/process", json=payload) as resp:
            data = await resp.json()
            print("Resultado:", data)

if __name__ == "__main__":
    asyncio.run(example_health_check())
