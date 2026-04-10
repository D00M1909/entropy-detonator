import os
import time

print("Initiating simulated ransomware attack...")
time.sleep(2)

try:
    for i in range(20):
        with open(f"target_directory/locked_data_{i}.dat", "wb") as f:
            f.write(os.urandom(1024 * 1024))

        print(f"Malware: Encrypted file {i}")
        time.sleep(0.1)

    print("Attack finished (If you see this, the Detonator failed!)")
except Exception as e:
    print(f"Attack forcefully terminated by the system! Error: {e}")
