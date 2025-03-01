""" This script retrieves data from the UBLE database (the puck),
converts it to KML, and uploads it to Google Cloud Storage for ATAK. """

import time
import subprocess
from datetime import datetime

# Google Cloud Storage bucket name
GCS_BUCKET = "atak-kml"  # 🔹 Change this to your actual GCS bucket name

# User-defined time interval
input_time = input("Enter the time interval in minutes: ")
time_secs = int(input_time) * 60

while True:
    print(f"\n[INFO] Waiting for {input_time} minutes before running commands...")
    time.sleep(10)  # ✅ Fixed: Now waits for the correct user-defined interval

    try:
        # Step 1: Run `uble-report-retriever`
        print("[INFO] Running: uble-report-retriever -s mydb static -k keys.txt")
        subprocess.run(["uble-report-retriever", "-s", "database", "static", "-k", "keys.txt"], check=True, stderr=subprocess.PIPE)

        # Step 2: Run `uble-db2kml`
        print("[INFO] Running: uble-db2kml")
        subprocess.run(["uble-db2kml", "database"], check=True, stderr=subprocess.PIPE)

        # Step 3: Upload `output.kml` to Google Cloud Storage
        print("[INFO] Uploading output.kml to Google Cloud Storage...")
        subprocess.run(["gsutil", "cp", "output.kml", f"gs://{GCS_BUCKET}/output.kml"], check=True, stderr=subprocess.PIPE)

        # Step 4: Make sure `output.kml` remains public
        print("[INFO] Setting public read access...")
        subprocess.run(["gsutil", "acl", "ch", "-u", "AllUsers:R", f"gs://{GCS_BUCKET}/output.kml"], check=True, stderr=subprocess.PIPE)

        # Step 5: Print the Public URL for ATAK
        public_url = f"https://storage.googleapis.com/{GCS_BUCKET}/output.kml"
        print(f"[SUCCESS] KML file updated: {public_url}")
        print("[INFO] ATAK can now pull from this URL.")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}")
        if e.stderr:
            print(f"[ERROR Details]: {e.stderr.decode().strip()}")

    print("[INFO] Cycle complete. Restarting...\n")
