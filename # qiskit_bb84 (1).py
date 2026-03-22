# qiskit_bb84.py
import random
import time
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

# --- Core Qiskit Functions ---

def prepare_photon(bit, basis):
    """
    Simulates Alice preparing a single-qubit quantum circuit.
    - Rectilinear ('+'): |0> or |1>
    - Diagonal ('x'): |+> or |->
    """
    qc = QuantumCircuit(1, 1)
    # Prepare the bit (0 or 1)
    if bit == 1:
        qc.x(0)  # Apply NOT gate for bit 1

    # Apply basis (Hadamard gate for diagonal basis)
    if basis == 'x':
        qc.h(0)

    # Note: We do NOT measure yet. The circuit is the "photon".
    return qc

def measure_photon(photon_circuit, bob_basis):
    """
    Simulates Bob measuring the photon circuit in his chosen basis.
    """
    # Create a new circuit to add Bob's measurement logic
    bob_circuit = photon_circuit.copy()

    # Apply basis (Hadamard gate to measure in the diagonal basis)
    if bob_basis == 'x':
        bob_circuit.h(0)

    # Measure the qubit
    bob_circuit.measure(0, 0)
    
    # Run the circuit on a quantum simulator
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(bob_circuit, simulator)
    job = simulator.run(transpiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(bob_circuit)

    # The result is a dictionary like {'0': 1} or {'1': 1}
    # We get the bit from the key of the dictionary
    return int(list(counts.keys())[0])

def eavesdrop(circuit_stream):
    """
    Simulates Eve intercepting and measuring each photon in a random basis.
    She re-prepares and sends a new photon based on her measurement.
    """
    print("🕵️ Eve is intercepting the photons...")
    tampered_stream = []
    for circuit in circuit_stream:
        # Eve randomly chooses a basis and measures
        eve_basis = random.choice(['+', 'x'])
        measured_bit = measure_photon(circuit, eve_basis)
        
        # Eve creates a NEW photon based on her measurement result
        tampered_stream.append(prepare_photon(measured_bit, eve_basis))
    print("🕵️ Eve has sent the tampered photons on to Bob.")
    return tampered_stream

# --- BB84 Protocol Simulation ---

def run_bb84_simulation(key_length, eavesdrop_on=False):
    """
    Executes the full BB84 protocol using Qiskit.
    """
    print("--- BB84 Qiskit Simulation ---")
    print(f"Key length to be created: {key_length} bits.\n")
    time.sleep(1)

    # 1. Alice's Preparation
    print("🟢 Step 1: Alice's Preparation")
    alice_bits = [random.randint(0, 1) for _ in range(key_length)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(key_length)]
    
    alice_circuits = [
        prepare_photon(alice_bits[i], alice_bases[i])
        for i in range(key_length)
    ]
    print(f"Alice's secret bits: {alice_bits}")
    print(f"Alice's chosen bases: {alice_bases}")
    print("Alice prepares and sends photons to Bob.\n")
    time.sleep(1)

    # 2. Bob's Measurement
    print("🟡 Step 2: Bob's Measurement")
    
    # Optional: Eavesdropper enters the channel
    if eavesdrop_on:
        alice_circuits = eavesdrop(alice_circuits)
    
    bob_bases = [random.choice(['+', 'x']) for _ in range(key_length)]
    bob_bits = [
        measure_photon(alice_circuits[i], bob_bases[i])
        for i in range(key_length)
    ]
    print(f"Bob's chosen bases: {bob_bases}")
    print(f"Bob's measurement results: {bob_bits}")
    print("Bob has measured the photons.\n")
    time.sleep(1)

    # 3. Sifting the Key
    print("✨ Step 3: Sifting the Key")
    alice_sifted_key = []
    bob_sifted_key = []
    
    for i in range(key_length):
        if alice_bases[i] == bob_bases[i]:
            alice_sifted_key.append(alice_bits[i])
            bob_sifted_key.append(bob_bits[i])
    
    print("Alice and Bob publicly compare their bases and discard mismatches.")
    print(f"Alice's sifted key: {alice_sifted_key}")
    print(f"Bob's sifted key:   {bob_sifted_key}")
    print("The sifted keys now match, forming a shorter shared key.\n")
    time.sleep(1)

    # 4. Error Checking & Final Key
    print("🔬 Step 4: Error Checking")
    
    if len(alice_sifted_key) < 5:
        print("Sifted key is too short to perform error checking.")
        return

    sample_size = int(len(alice_sifted_key) * 0.20)
    sample_indices = random.sample(range(len(alice_sifted_key)), sample_size)
    
    errors = 0
    for i in sample_indices:
        if alice_sifted_key[i] != bob_sifted_key[i]:
            errors += 1
    
    qber = (errors / sample_size) * 100
    
    print(f"Comparing a random sample of {sample_size} bits...")
    print(f"Number of errors found: {errors}")
    print(f"Quantum Bit Error Rate (QBER): {qber:.2f}%")
    
    if qber > 11:
        print("\n🚨 HIGH ERROR RATE DETECTED! Eavesdropping is suspected.")
        print("The protocol is compromised. The key is discarded.")
        return

    print("\n✅ Low error rate. The key is secure!")
    
    final_key_alice = [
        bit for i, bit in enumerate(alice_sifted_key)
        if i not in sample_indices
    ]
    
    final_key_bob = [
        bit for i, bit in enumerate(bob_sifted_key)
        if i not in sample_indices
    ]
    
    print(f"\n🔐 Final Shared Secure Key (Alice's side): {final_key_alice}")
    print(f"🔐 Final Shared Secure Key (Bob's side):   {final_key_bob}")
    print("\nThe remaining bits form the final, secure key for communication.")

# --- Run the Simulation ---
if __name__ == "__main__":
    print("Running simulation with NO eavesdropping...")
    run_bb84_simulation(key_length=100, eavesdrop_on=False)
    
    print("\n" + "="*70 + "\n")
    
    print("Running simulation WITH eavesdropping...")
    run_bb84_simulation(key_length=100, eavesdrop_on=True)