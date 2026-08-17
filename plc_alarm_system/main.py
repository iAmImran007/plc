import asyncio
import threading
from process_data.process import dummy_plc, audio_manager_thread
#from connect.connection import connect_plc


async def main():
    asyncio.create_task(asyncio.to_thread(audio_manager_thread))
    
    #await connect_plc()
    await dummy_plc() 



if __name__ == "__main__":
    asyncio.run(main())
    


