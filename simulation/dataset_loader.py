"""
Industrial Manufacturing Defect Dataset Loader Simulator
Simulates MVTec AD / NEU Surface Defect datasets (Metal, Steel, PCB, Plastic)
"""

import numpy as np

class IndustrialDatasetSimulator:
    def __init__(self, image_shape=(224, 224)):
        self.image_shape = image_shape
        self.categories = ["metal_surface", "steel_sheet", "pcb_circuit", "plastic_molding"]

    def generate_batch(self, num_samples=10, defect_ratio=0.4):
        """
        Generates simulated industrial inspection frames with controllable defect noise & structural anomalies.
        """
        samples = []
        for i in range(num_samples):
            category = self.categories[i % len(self.categories)]
            is_defect = (i / num_samples) < defect_ratio

            # Base normal surface image
            img = np.random.normal(loc=128.0, scale=10.0, size=self.image_shape).astype(np.uint8)

            if is_defect:
                # Add visual surface defect patterns (high variance region or scratch intensity)
                noise_type = i % 3
                if noise_type == 0:
                    # High variance scratch
                    img[50:150, 50:150] = np.random.normal(loc=200.0, scale=55.0, size=(100, 100))
                elif noise_type == 1:
                    # Cracks / Inclusions
                    img[80:120, 80:180] = np.random.normal(loc=30.0, scale=48.0, size=(40, 100))
                else:
                    # Zero-shot unseen structural anomaly
                    img[10:100, 10:100] = np.random.normal(loc=160.0, scale=38.0, size=(90, 90))

            samples.append({
                "sample_id": i + 1,
                "category": category,
                "is_ground_truth_defect": is_defect,
                "image_array": img
            })

        return samples
