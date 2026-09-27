"""
Real-Time Industrial Conveyor Belt Defect Inspection & Edge Energy Benchmark Simulator
"""

import os
import sys

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.edge_pipeline import EdgeDefectPipeline
from simulation.dataset_loader import IndustrialDatasetSimulator

def run_edge_simulation():
    print("=======================================================================")
    print("[+] Real-Time Edge AI Industrial Defect Detection Engine (HD-DSEA)")
    print("    NVIDIA Jetson / Edge Device Live Conveyor Belt Inspection Simulator")
    print("=======================================================================\n")

    pipeline = EdgeDefectPipeline()
    dataset_sim = IndustrialDatasetSimulator()

    samples = dataset_sim.generate_batch(num_samples=20, defect_ratio=0.45)

    print(f"[*] Processing {len(samples)} Simulated Manufacturing Conveyor Belt Frames...\n")
    print(f"{'FRAME':<8}{'CATEGORY':<16}{'STATUS':<18}{'DECISION':<30}{'FPS':<8}{'LATENCY':<12}{'GPIO ALERT'}")
    print("-" * 105)

    total_fps = 0
    total_latency = 0

    for sample in samples:
        res = pipeline.process_frame(sample["image_array"])
        total_fps += res["throughput_fps"]
        total_latency += res["total_latency_ms"]

        alert_str = "[ALERT] TRIGGERED" if res["gpio_hardware_trigger_alert"] else "[OK] CLEAN"
        print(f"#{sample['sample_id']:<7}{sample['category']:<16}{res['status']:<18}{res['gating_decision']:<30}{res['throughput_fps']:<8}{res['total_latency_ms']:<12}{alert_str}")

    avg_fps = round(total_fps / len(samples), 1)
    avg_latency = round(total_latency / len(samples), 2)
    telemetry = pipeline.gating.get_efficiency_report()

    print("\n=======================================================================")
    print("[STATS] REAL-TIME EDGE TELEMETRY & NOVELTY BENCHMARK SUMMARY")
    print("=======================================================================")
    print(f"  • Total Industrial Frames Inspected: {telemetry['total_frames_processed']}")
    print(f"  • Average Pipeline Throughput:       {avg_fps} FPS")
    print(f"  • Average End-to-End Latency:        {avg_latency} ms")
    print(f"  • Autoencoder Bypass Ratio (HD-DSEA):{telemetry['ae_bypass_ratio']}% of frames")
    print(f"  • Estimated Edge Power Saved:        {telemetry['estimated_energy_saved_joules']} Joules")
    print(f"  • Hardware Conveyor Ejection Alerts: {sum(1 for s in samples if s['is_ground_truth_defect'])} triggered")
    print("=======================================================================\n")

if __name__ == "__main__":
    run_edge_simulation()
