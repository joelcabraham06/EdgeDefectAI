"""
Real-Time Edge AI Industrial Defect Detection Engine
Novelty Module: Hybrid-DynaGated Dual-Stream Edge Architecture (HD-DSEA)
Dynamic Gating Controller & Uncertainty-Driven Execution Stream
"""

class DynamicGatingController:
    def __init__(self, high_conf_thresh=0.85, low_conf_thresh=0.25):
        self.high_conf_thresh = high_conf_thresh
        self.low_conf_thresh = low_conf_thresh
        
        # Telemetry metrics
        self.total_frames = 0
        self.bypassed_ae_count = 0
        self.gated_ae_count = 0
        self.energy_saved_joules = 0.0

    def evaluate_gate(self, yolo_result):
        """
        Evaluates frame uncertainty U(x) to decide whether to activate
        the secondary Latent Reconstruction Stream.
        """
        self.total_frames += 1
        conf = yolo_result["confidence_score"]
        has_known = yolo_result["has_known_defect"]

        # High confidence known defect OR clear high-confidence normal frame -> BYPASS Autoencoder
        if (has_known and conf >= self.high_conf_thresh) or (not has_known and conf <= self.low_conf_thresh):
            self.bypassed_ae_count += 1
            self.energy_saved_joules += 0.45 # ~0.45 Joules saved per frame bypass on Jetson
            return {
                "activate_reconstruction_stream": False,
                "gate_decision": "BYPASS_AE_FAST_PATH",
                "reason": "High confidence prediction; secondary stream bypassed to optimize FPS & wattage."
            }

        # Uncertainty region -> TRIGGER Latent Reconstruction Stream for Zero-Shot Anomaly Verification
        self.gated_ae_count += 1
        return {
            "activate_reconstruction_stream": True,
            "gate_decision": "TRIGGER_LATENT_RECONSTRUCTION",
            "reason": "Frame in uncertainty region (0.25 < C < 0.85). Triggering zero-shot anomaly check."
        }

    def get_efficiency_report(self):
        bypass_percent = (self.bypassed_ae_count / max(1, self.total_frames)) * 100
        return {
            "total_frames_processed": self.total_frames,
            "bypassed_ae_frames": self.bypassed_ae_count,
            "gated_ae_frames": self.gated_ae_count,
            "ae_bypass_ratio": round(bypass_percent, 2),
            "estimated_energy_saved_joules": round(self.energy_saved_joules, 2)
        }
