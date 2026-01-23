import asyncio
import aiosqlite

async def main():
    async with aiosqlite.connect('artemisops.db') as db:
        async with db.execute('SELECT patch_url, agency_logo_url, image_url FROM missions WHERE id LIKE ?', ('%artemis-ii%',)) as cursor:
            row = await cursor.fetchone()
            if row:
                print(f"patch_url: {row[0]}")
                print(f"agency_logo_url: {row[1]}")
                print(f"image_url: {row[2]}")
            else:
                print("No artemis-ii found")

asyncio.run(main())
