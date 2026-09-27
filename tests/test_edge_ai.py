"""
Automated Pytest / Verification Test Suite for EdgeDefectAI
"""

import unittest
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.detector import YOLOEdgeDetector
from engine.anomaly_ae import LatentReconstructionAE
from engine.dynamic_gating import DynamicGatingController
from engine.edge_pipeline import EdgeDefectPipeline
from simulation.dataset_loader import IndustrialDatasetSimulator

class TestEdgeDefectAI(unittest.TestCase):
    def setUp(self):
        self.detector = YOLOEdgeDetector()
        self.anomaly_ae = LatentReconstructionAE()
        self.gating = DynamicGatingController()
        self.pipeline = EdgeDefectPipeline()
        self.dataset_sim = IndustrialDatasetSimulator()

    def test_detector_inference(self):
        img = np.random.normal(loc=128.0, scale=50.0, size=(224, 224))
        res = self.detector.detect(img)
        self.assertIn("detections", res)
        self.assertGreater(res["inference_time_ms"], 0)

    def test_anomaly_reconstruction(self):
        img = np.random.normal(loc=128.0, scale=10.0, size=(224, 224))
        res = self.anomaly_ae.compute_reconstruction_error(img)
        self.assertIn("reconstruction_mse", res)
        self.assertIn("is_zero_shot_anomaly", res)

    def test_dynamic_gating_bypass(self):
        yolo_high_conf = {"has_known_defect": True, "confidence_score": 0.95}
        gate_res = self.gating.evaluate_gate(yolo_high_conf)
        self.assertFalse(gate_res["activate_reconstruction_stream"])
        self.assertEqual(gate_res["gate_decision"], "BYPASS_AE_FAST_PATH")

    def test_dynamic_gating_trigger(self):
        yolo_uncertain = {"has_known_defect": False, "confidence_score": 0.50}
        gate_res = self.gating.evaluate_gate(yolo_uncertain)
        self.assertTrue(gate_res["activate_reconstruction_stream"])
        self.assertEqual(gate_res["gate_decision"], "TRIGGER_LATENT_RECONSTRUCTION")

    def test_end_to_end_pipeline(self):
        samples = self.dataset_sim.generate_batch(num_samples=5)
        for s in samples:
            res = self.pipeline.process_frame(s["image_array"])
            self.assertIn(res["status"], ["CLEAN", "DEFECT_DETECTED"])
            self.assertGreater(res["throughput_fps"], 0)

if __name__ == "__main__":
    unittest.main()
