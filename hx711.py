import time
import sys
import supabase
from hx711 import HX711

# Initialize Supabase client
supabase_url = "https://fwnwsgwxofkspxidiipf.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ3bndzZ3d4b2Zrc3B4aWRpaXBmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTE3MzIzNDYsImV4cCI6MjAyNzMwODM0Nn0.QYN5Cjb4YNmO9x8h2XlI0-D5cq6sG8dKqM5ip7R-VvE"
supabase_client = supabase.create_client(supabase_url, supabase_key)

# Initialize HX711 sensor
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
referenceUnit = 114
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare done! Add weight now...")

def clean_and_exit():
    print("Cleaning...")
    print("Bye!")
    sys.exit()

while True:
    try:
        # Measure weight
        val = hx.get_weight(5)
        print(val)

        # Fetch all weights from the table
        weights = supabase_client.table('weights').select('id, weight').execute().get('data', [])
        # If there are more than 10 weights, delete the oldest one
        if len(weights) >= 10:
            oldest_id = min(weights, key=lambda x: x['id'])['id']
            supabase_client.table('weights').delete().eq('id', oldest_id).execute()

        # Insert new weight
        supabase_client.table('weights').insert({'weight': val}).execute()

        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()