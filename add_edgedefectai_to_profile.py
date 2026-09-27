import base64
import httpx
import sys

GITHUB_USERNAME = "joelcabraham06"
REPO_NAME = GITHUB_USERNAME

UPDATED_PROFILE_README = """<div align="center">

# 👨‍💻 Joel C. Abraham
### **Hardware-Software Engineer | Embedded AI, IoT & Computer Vision Specialist**

🎓 **B.Tech in Electronics & Communication Engineering (ECE)**  
🏛️ **Amrita School of Engineering** (Amrita Vishwa Vidyapeetham)  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-joelcabraham06-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/joelcabraham06)
[![Email](https://img.shields.io/badge/Email-joelcabraham21%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:joelcabraham21@gmail.com)

<br/>

<img src="https://img.shields.io/badge/Focus-Embedded%20AI%20%7C%20IoT%20%7C%20Computer%20Vision%20%7C%20Software%20Development-00f0ff?style=for-the-badge" alt="Focus Banner" />

</div>

---

## 👋 About Me

I am a **Hardware-Software Engineer** bridging the gap between embedded hardware, real-time edge processing, computer vision, and scalable software systems. My academic and research work centers on **embedded AI, IoT energy monitoring, sensor drift recalibration, and intelligent autonomous systems**.

- 🔭 **Current Focus**: Embedded AI, Edge Vision Accelerators, ESP32 IoT Architectures, Computer Vision (OpenCV/YOLO), and Real-Time Signal Processing.
- 🔬 **Primary Research**: Time-dependent Gas Sensor Array Drift Compensation & Edge Anomaly Gating Architectures.
- 🎯 **Career Target**: Embedded AI Engineer / Software Development Engineer (SDE) / Computer Vision Specialist.

---

## ⚡ Featured Flagship Projects

### ⚡ 1. [EdgeDefectAI – Real-Time Edge AI Industrial Defect Detection Engine](https://github.com/joelcabraham06/EdgeDefectAI)
> **Novel Architecture**: Hybrid-DynaGated Dual-Stream Edge Architecture (HD-DSEA) combining supervised YOLOv8 detection with unsupervised reconstruction-residual autoencoders for zero-shot manufacturing defect detection on Edge Hardware (NVIDIA Jetson).

- 🚀 **Performance**: **45+ FPS Throughput**, **58% Reduced Edge Energy**, and **100% Zero-Shot Anomaly Recall**.
- 🛠️ **Tech**: Python, YOLOv8-Lite, Autoencoders, TensorRT Optimization, GPIO Hardware Triggers.

### 🔌 2. Smart Grid Power & Energy Management System
> **IoT Energy Analytics**: Real-time AC voltage/current measurement (ZMPT101B + ACS712), automated relay surge protection, and Blynk/Firebase cloud telemetry.
- 🛠️ **Tech**: ESP32, Sensors, Relays, Blynk IoT, Firebase, C++, Node.js.

---

## 🔬 Research & Advanced Systems

### 🧪 1. Gas Sensor Array Drift Detection & Recalibration
- **Dataset**: Gas Sensor Array Drift Dataset (13,910 measurements, 16 sensors, 128 features across 10 temporal batches).
- **Novelty**: Persistence-aware, severity-controlled recalibration using **Autoencoder Reconstruction Error monitoring**, Incremental PCA, and energy-aware scheduling.

### 🤖 2. JARVIS Autonomous Voice & Vision AI Assistant
- **Tech**: Python, OpenCV, YOLO Object Detection, Speech Recognition, PyTTSx3, REST APIs.

### 📜 3. Janaseva – Multilingual WhatsApp Government Service Assistant
- **Tech**: Python, FastAPI, React 18, WhatsApp Cloud API, PostgreSQL, Redis, Docker.

---

## 🛠️ Technical Skill Matrix

| Category | Skills & Technologies |
|---|---|
| **Embedded & IoT** | ESP32, Arduino UNO, NodeMCU, FreeRTOS, ZMPT101B, ACS712, MQ-2, Relays, Blynk, Firebase, ThingSpeak |
| **Edge AI & Vision** | YOLOv8, TensorRT, Autoencoders, Anomaly Detection, OpenCV, TensorFlow/Keras, scikit-learn |
| **Programming** | C++, Python, JavaScript (Node.js/Express), C, SQL, MATLAB |
| **Electronics & VLSI** | Analog Electronics, Communication Theory, Control Systems, Cadence Virtuoso, LTspice, SPICE Simulation |
| **Signal Processing** | MATLAB, DSP, FFT, DTFT, FIR/IIR Butterworth & Chebyshev Filters, Bilinear Transform |
| **Software & DevOps** | Data Structures & Algorithms (DSA), OOP, DBMS, OS, Git/GitHub, Linux, Docker, Postman, Nginx |

---

## 📊 GitHub & Activity Statistics

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=joelcabraham06&show_icons=true&theme=tokyonight" alt="Joel's GitHub Stats" width="48%" />
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=joelcabraham06&layout=compact&theme=tokyonight" alt="Top Languages" width="48%" />
</p>

---

<div align="center">

### 🤝 Let's Connect & Collaborate!

[![Email](https://img.shields.io/badge/Email-joelcabraham21%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:joelcabraham21@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-joelcabraham06-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/joelcabraham06)

*⚡ "Bridging Hardware and Intelligent Software to Build High-Impact Systems."*

</div>
"""

def update_profile(pat_token):
    headers = {
        "Authorization": f"Bearer {pat_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/README.md"
        get_res = client.get(url, headers=headers)
        sha = None
        if get_res.status_code == 200:
            sha = get_res.json().get("sha")

        content_b64 = base64.b64encode(UPDATED_PROFILE_README.encode("utf-8")).decode("utf-8")
        payload = {
            "message": "Add EdgeDefectAI project to profile README",
            "content": content_b64,
            "branch": "main"
        }
        if sha:
            payload["sha"] = sha

        put_res = client.put(url, headers=headers, json=payload)
        if put_res.status_code in (200, 201):
            print(f"[OK] Profile README updated at https://github.com/{GITHUB_USERNAME}/{REPO_NAME}!")
            return True
        else:
            print(f"[FAIL] Error updating profile README: {put_res.status_code} - {put_res.text}")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_edgedefectai_to_profile.py <PAT_TOKEN>")
        sys.exit(1)
    update_profile(sys.argv[1])
