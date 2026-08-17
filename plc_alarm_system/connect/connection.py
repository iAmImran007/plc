import snap7
import asyncio
import snap7.util
from process_data.process import process_plc_output

#plc bool tags dect
DATA = {}

#plc connection 
async def connect_plc():
    #change plc_ip, rack, slot acording to you
    plc_ip = "192.168.1.10" 
    rack, slot = 0, 1
    reconnect_delay = 3  

    while True:
        print(f"Attempting to connect to PLC at {plc_ip}...")
        try:
            async with snap7.AsyncClient() as client:
                await client.connect(plc_ip, rack, slot)
                print("PLC Connection established.")

                while True:
                    try:
                        raw_db_data = await client.db_read(1, 0, 4)
                        if raw_db_data:
                            DATA["Emergency_Stop"] = snap7.util.get_bool(raw_db_data, 0, 0)
                            #add more feilds acording to you
                            
                    except Exception as read_err:
                        print(f"PLC read error detected: {read_err}")
                        break  

                    await asyncio.sleep(0.5)  # Poll interval

        except Exception as conn_err:
            print(f"PLC connection failed: {conn_err}")

        # Wait before attempting to reconnect
        print(f"Reconnecting in {reconnect_delay} seconds...")
        await asyncio.sleep(reconnect_delay)
