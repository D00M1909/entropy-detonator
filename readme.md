![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Category](https://img.shields.io/badge/domain-Cybersecurity-red)
![Heuristic](https://img.shields.io/badge/detection-Shannon%20Entropy-orange)

# Entropy Detonator: Heuristic Ransomware Interceptor

## Overview
Entropy Detonator is a Proof-of-Concept (PoC) security tool that stops zero-day ransomware in real-time. Instead of relying on known malware signatures, it uses **Shannon Entropy** to detect the mathematical randomness caused by unauthorized file encryption, killing the malicious process before data is lost.

## Why Behavior Over Signatures?
Traditional antivirus relies on cataloged signatures, which ransomware easily evades by obfuscating code. Entropy Detonator shifts to **behavioral blocking**—stopping the encryption action itself.

## The Math: Shannon Entropy
Strong encryption (like AES-256) scrambles data into maximum randomness. We measure this randomness using Shannon Entropy:

$$H(X) = - \sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

Where `P(x_i)` is the probability of a specific byte appearing in the data stream.

* **Standard Files:** Plaintext and standard documents usually score **3.0 to 5.0** (out of 8.0).
* **Encrypted Files:** Scrambled data hits the maximum entropy score (**near 8.0**).

## The 4-Stage Pipeline

1. **Monitor (I/O Hooking):** Uses `watchdog` to listen for file creations and modifications in a target directory.
2. **Calculator (Math):** Instantly calculates the Shannon Entropy score of the modified file.
3. **Logic Gate (Heuristic):** Prevents false positives (like video compression) by checking speed. Triggers only if **$\ge$ 3 files** with an entropy **> 7.5** are generated within **2.0 seconds**.
4. **Executioner (Process Kill):** Uses `psutil` to track down the offending process, suspends it, and kills the entire process tree to stop the attack.

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