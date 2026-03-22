# BB84 Quantum Key Distribution 🔐

A Python implementation of the **BB84 Quantum Key Distribution (QKD) protocol** using IBM's **Qiskit** framework — simulating secure quantum cryptographic key exchange between two parties (Alice and Bob).

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.x-6929C4?style=flat-square&logo=qiskit&logoColor=white)](https://qiskit.org)
[![Quantum](https://img.shields.io/badge/Topic-Quantum%20Cryptography-00B4D8?style=flat-square)]()

---

## What is BB84?

**BB84** (Bennett & Brassard, 1984) is the world's first and most widely studied **quantum key distribution protocol**. It allows two parties — traditionally called **Alice** and **Bob** — to generate a shared secret key over a quantum channel, with security guaranteed by the laws of quantum mechanics.

Any eavesdropper (Eve) attempting to intercept the key will **inevitably disturb the quantum states**, making her presence detectable.

---

## How It Works

```
Alice                        Quantum Channel                        Bob
  │                                                                   │
  │── Encodes random bits ──►  |0⟩ |1⟩ |+⟩ |−⟩  ──► Measures qubits ─│
  │   in random bases (+ or ×)                      in random bases   │
  │                                                                   │
  │◄────────────── Classical Channel (Public) ───────────────────────►│
  │                  Compare bases (not bits!)                        │
  │                                                                   │
  │           Keep only bits where bases matched                      │
  │◄─────────────────── Sifted Key ─────────────────────────────────►│
```

### Step-by-Step Protocol

| Step | Description |
|------|-------------|
| **1. Qubit Preparation** | Alice randomly chooses bits (0 or 1) and bases (rectilinear `+` or diagonal `×`) |
| **2. Qubit Transmission** | Alice encodes each bit as a qubit and sends it over the quantum channel |
| **3. Measurement** | Bob randomly chooses a basis and measures each received qubit |
| **4. Basis Reconciliation** | Alice and Bob publicly compare their chosen bases (NOT the bits) |
| **5. Key Sifting** | Both keep only the bits where their bases matched (~50% of qubits) |
| **6. Eavesdropping Check** | Compare a subset of the sifted key — any mismatch reveals Eve |
| **7. Final Key** | Remaining bits form the secret shared key |

---

## Quantum States Used

| Bit | Basis `+` (Rectilinear) | Basis `×` (Diagonal) |
|-----|------------------------|----------------------|
| 0   | `\|0⟩` (no gate)        | `\|+⟩` (H gate)       |
| 1   | `\|1⟩` (X gate)         | `\|−⟩` (X then H)     |

---

## Prerequisites

```bash
pip install qiskit
pip install qiskit-aer
pip install matplotlib
pip install numpy
```

Or install all at once:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
qiskit>=1.0.0
qiskit-aer>=0.14.0
matplotlib>=3.7.0
numpy>=1.24.0
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/qiskit-bb84.git
cd qiskit-bb84

# Install dependencies
pip install -r requirements.txt

# Run the simulation
python qiskit_bb84.py
```

---

## Usage

```python
# Run a basic BB84 simulation with 20 qubits
python qiskit_bb84.py

# Example output:
# Alice's bits    : [1, 0, 1, 1, 0, 0, 1, 0, ...]
# Alice's bases   : [+, ×, ×, +, +, ×, ×, +, ...]
# Bob's bases     : [×, ×, +, +, ×, ×, ×, +, ...]
# Bob's results   : [?, 0, ?, 1, ?, ?, 1, 0, ...]
#
# Matching bases  : indices [1, 3, 6, 7, ...]
# Sifted key      : [0, 1, 1, 0, ...]
#
# No eavesdropping detected!
# Final shared key: [0, 1, 1, 0, ...]
```

---

## Project Structure

```
qiskit-bb84/
├── qiskit_bb84.py       ← Main BB84 protocol implementation
├── requirements.txt     ← Python dependencies
└── README.md            ← This file
```

---

## Key Concepts Demonstrated

- **Quantum Superposition** — Qubits exist in multiple states simultaneously until measured
- **No-Cloning Theorem** — Quantum states cannot be copied, preventing perfect eavesdropping
- **Measurement Collapse** — Measuring a qubit in the wrong basis destroys the original state
- **Eavesdropping Detection** — Any interception introduces a ~25% error rate in the sifted key

---

## Security Guarantees

| Threat | BB84 Defense |
|--------|-------------|
| Eavesdropping (Eve measures and resends) | Introduces ~25% QBER — detected during check phase |
| Man-in-the-middle attack | Detected via QBER and authentication |
| Classical brute-force | Key length scales with qubit count |
| Copying qubits | Impossible — No-Cloning Theorem |

> **QBER** = Quantum Bit Error Rate. If QBER > ~11%, the channel is considered compromised and the key is discarded.

---

## Simulation vs Real Quantum Hardware

| Feature | Simulation (Qiskit Aer) | Real IBM Quantum |
|---------|------------------------|-----------------|
| Noise | None (ideal) | Hardware noise |
| Speed | Fast | Queue-based |
| Access | Local | IBM Quantum Network |
| Accuracy | 100% | ~95-99% |

To run on real IBM Quantum hardware:
```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False)
```

---

## Sample Output

```
╔══════════════════════════════════════════════╗
║         BB84 QKD Simulation Results          ║
╠══════════════════════════════════════════════╣
║  Qubits sent          : 20                   ║
║  Matching bases       : 9                    ║
║  Sifted key length    : 9 bits               ║
║  QBER                 : 0.00%                ║
║  Eavesdropping        : Not detected         ║
║  Final key            : 011010110            ║
╚══════════════════════════════════════════════╝
```

---

## Extending the Project

- **Add Eve** — Simulate an eavesdropper intercepting qubits and measure QBER increase
- **Privacy Amplification** — Shorten the key to reduce Eve's partial information
- **Error Correction** — Implement Cascade or LDPC error correction on the sifted key
- **BB84 with Noise** — Use `qiskit-aer` noise models to simulate real hardware
- **E91 Protocol** — Implement Ekert's entanglement-based QKD variant
- **Visualization** — Plot Bloch spheres for each qubit state

---

## References

- Bennett, C.H. & Brassard, G. (1984). *Quantum cryptography: Public key distribution and coin tossing.*
- [Qiskit Documentation](https://docs.quantum.ibm.com/)
- [IBM Quantum Learning](https://learning.quantum.ibm.com/)
- [Quantum Key Distribution — Wikipedia](https://en.wikipedia.org/wiki/Quantum_key_distribution)

---

## License

MIT License — free to use, modify, and distribute.

---

*Simulating quantum security, one qubit at a time.*
