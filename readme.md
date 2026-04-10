# Entropy Detonator: Heuristic Ransomware Interceptor

## Overview
Entropy Detonator is a Proof-of-Concept (PoC) endpoint security tool designed to halt zero-day ransomware attacks in real-time. Rather than relying on static malware signatures, this system utilizes fundamental information theory—specifically Shannon Entropy—to detect the behavioral footprint of unauthorized file encryption. Upon detecting anomalous cryptographic activity, the system isolates and terminates the offending process tree before catastrophic data loss can occur.

## The Problem: Signature Evasion
Traditional antivirus (AV) and Intrusion Detection Systems (IDS) rely on identifying known malicious code signatures. Ransomware developers circumvent this by constantly obfuscating or recompiling their payloads. By the time a new variant's signature is cataloged, the endpoint has already been compromised. 

Entropy Detonator shifts the defensive paradigm from **code-scanning** to **behavioral blocking**.

## Mathematical Foundation: Shannon Entropy
To hold data for ransom, an attacker must encrypt it. Strong encryption algorithms (e.g., AES-256) fundamentally destroy data patterns, resulting in a state of maximum mathematical randomness. This randomness is measured using Shannon Entropy.

The system calculates the entropy of a file by analyzing its byte frequency distribution (values 0-255) using the following formula:

$$H(X) = - \sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

*Where $P(x_i)$ is the probability of a specific byte appearing in the data stream.*

* **Standard Files (Low/Medium Entropy):** Plaintext, standard documents, and system logs contain repeating patterns. They typically yield an entropy score between 3.0 and 5.0 out of 8.0.
* **Encrypted Files (High Entropy):** Cryptographically scrambled data forces an equal probability distribution across all byte values, pushing the entropy score to its mathematical maximum (near 8.0).

## System Architecture & Logic
The interceptor operates through a four-stage pipeline:

1.  **The Monitor (I/O Hooking):**
    Utilizing the Python `watchdog` library, the system establishes a low-overhead hook on a designated target directory. It listens asynchronously for `FileCreated` and `FileModified` OS-level events.
2.  **The Calculator (Cryptographic Analysis):**
    Upon event triggering, the system reads the modified file in binary mode. It instantly generates a byte-frequency map and computes the Shannon Entropy score.
3.  **The Logic Gate (Temporal Heuristic Engine):**
    High entropy alone is insufficient for detection (e.g., legitimate user compression or video rendering also yields high entropy). To eliminate false positives, the system enforces a strict temporal heuristic:
    * **Threshold:** Entropy > 7.5
    * **Velocity:** $\ge$ 3 high-entropy files generated within a 2.0-second rolling window.
4.  **The Executioner (Process Guillotine):**
    If the temporal heuristic is breached, the system traverses the active OS process list via `psutil`. It identifies the PID responsible for the unauthorized I/O operations, suspends it, maps its child processes, and issues a system-level kill command, halting the encryption cascade.

## Installation & Setup

**Prerequisites:**
* Python 3.8+
* Git

**Environment Setup:**
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/entropy-detonator.git](https://github.com/YOUR_USERNAME/entropy-detonator.git)
cd entropy-detonator

# Initialize and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt