"""
Real-Time Edge AI Industrial Defect Detection Engine
Module: Edge Processing Pipeline Orchestrator
"""

from .detector import YOLOEdgeDetector
from .anomaly_ae import LatentReconstructionAE
from .dynamic_gating import DynamicGatingController

class EdgeDefectPipeline:
    def __init__(self):
        self.detector = YOLOEdgeDetector()
        self.anomaly_ae = LatentReconstructionAE()
        self.gating = DynamicGatingController()

    def process_frame(self, image_array):
        """
        Executes HD-DSEA Dual-Stream Inspection on an incoming industrial frame.
        """
        # Step 1: Fast-Stream YOLO Detection
        yolo_res = self.detector.detect(image_array)

        # Step 2: Dynamic Gating Decision
        gate_res = self.gating.evaluate_gate(yolo_res)

        ae_res = None
        final_defect_status = "CLEAN"
        defect_category = "NONE"

        if yolo_res["has_known_defect"]:
            final_defect_status = "DEFECT_DETECTED"
            defect_category = f"SUPERVISED_{yolo_res['detections'][0]['class'].upper()}"

        # Step 3: Conditional Latent Reconstruction Stream
        if gate_res["activate_reconstruction_stream"]:
            ae_res = self.anomaly_ae.compute_reconstruction_error(image_array)
            if ae_res["is_zero_shot_anomaly"]:
                final_defect_status = "DEFECT_DETECTED"
                if defect_category == "NONE":
                    defect_category = "UNSUPERVISED_ZERO_SHOT_ANOMALY"

        total_latency_ms = yolo_res["inference_time_ms"] + (ae_res["inference_time_ms"] if ae_res else 0.0)
        fps = round(1000.0 / max(1.0, total_latency_ms), 1)

        return {
            "status": final_defect_status,
            "defect_category": defect_category,
            "yolo_detection": yolo_res,
            "gating_decision": gate_res["gate_decision"],
            "anomaly_reconstruction": ae_res,
            "total_latency_ms": round(total_latency_ms, 2),
            "throughput_fps": fps,
            "gpio_hardware_trigger_alert": final_defect_status == "DEFECT_DETECTED"
        }
