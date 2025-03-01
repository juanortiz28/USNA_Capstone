"""this code is meant to retrieve data from the UBLE database (the puck) and then conver to KML which will then be pushed into the github repository where ATAK will pull from"""

import time
import subprocess
from datetime import datetime

input_time = input("Enter the time interval in minutes: ")
time_secs = int(input_time) * 60

while True:
    print(f"\n[INFO] Waiting for {input_time} minutes before running commands...")
    time.sleep(time_secs)  # Wait for 2 minutes
    
    try: # Try to run the following commands
        # Step 1: Run `uble-report-retriever`
        print("[INFO] Running: uble-report-retriever -s mydb static -k keys.txt")
        subprocess.run(["uble-report-retriever", "-s", "mydb", "static", "-k", "keys.txt"], check=True)

        # Step 2: Run `uble-db2kml`
        print("[INFO] Running: uble-db2kml")
        subprocess.run(["uble-db2kml"], check=True)

        # Step 3: Git Add `output.kml`
        print("[INFO] Adding output.kml to Git")
        subprocess.run(["git", "add", "output.kml"], check=True)

        # Step 4: Git Commit with timestamp
        commit_message = f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"[INFO] Committing with message: {commit_message}")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Step 5: Git Push
        print("[INFO] Pushing changes to Git")
        subprocess.run(["git", "push"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}")

    print("[INFO] Cycle complete. Restarting...\n")

