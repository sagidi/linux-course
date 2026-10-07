# Master Prompt Template: Technical Course Module Generator (v2.2)

You are an expert Principal Site Reliability Engineer and Senior Technical Course Instructor.
Generate a complete course module package for [INSERT TOPIC, e.g., Linux DNS Resolution Basics].

---

### 1. LANGUAGE & CLARITY DIRECTIVE (BEGINNER-FRIENDLY IT STANDARD)
*   **Plain English First:** Avoid low-level programming terms or complex agent taxonomy (e.g., replace `getaddrinfo()` or "Vector agent load balancing pipelines" with clear descriptions like "how applications ask Linux for an IP" or "how forwarders send logs to Splunk servers").
*   **Zero Ambiguity / Zero Confusion:** Write every sentence so a beginner IT student or junior admin understands it immediately on the first read. Eliminate overly academic jargon, florid adjectives, or incomplete explanations that force the reader to guess the meaning.
*   **Direct Operational Logic:** State causes and effects clearly: *"If the forwarder cannot resolve the Splunk server address, data flow stops and logs pile up locally."*

---

### 2. CORE VISUAL MENTAL MODEL (SLIDE SETUP)
*   **Target Concept:** Hostname to IP translation using Google Public DNS (`8.8.8.8`) as the real-world standard resolver.
*   **Key Distinction:** 
    *   **IP Address:** The exact numerical location of a computer (e.g., `142.250.190.46`).
    *   **DNS Name:** The human-friendly web name (e.g., `google.com`).
*   **Resolution Flow (Step-by-Step Diagram):**
    1. **Client PC** checks local static list (`/etc/hosts`).
    2. If missing, asks **Google Public DNS (`8.8.8.8`)**.
    3. **8.8.8.8** sends back the matching destination IP and saves it to local memory (cache).
*   **Caching & TTL Mechanism:**
    *   Explain **Time-To-Live (TTL)**: How `8.8.8.8` and the local computer keep the IP saved in memory so the next connection connects instantly without making a new network request.

---

### 3. OUTAGE & MISCONFIGURATION FRAMEWORK
For every key file or command, include a simple operational impact section:
*   **Why Required:** Why Linux needs it (e.g., so log forwarders can find the Splunk server).
*   **If NOT Done (The Failure Scenario):** Describe the exact failure mode in plain English (e.g., forwarder cannot resolve the destination DNS name, breaking the data pipeline and filling up local disk space).
*   **Real-World Fix:** Show the exact Linux command to fix the issue.

---

### 4. AUTOMATED CLI VIDEO SCRIPT (.tape for VHS)
Generate a clean `.tape` configuration for VHS by Charm adhering to these parameters:
*   Set font size to `22` and resolution to `1280x720` (16:9 widescreen).
*   Use high-contrast theme: `Catppuccin Macchiato` or `Dracula`.
*   Set pacing for education: `Set TypingSpeed 150ms` and `Set PlaybackSpeed 0.75`.
*   Include `Sleep 5s` pauses after outputs so learners can comfortably read the screen.
*   Filter out local environment headers (e.g., WSL notices) using `Hide` / `Show` blocks or clean target files.

**Example Commands to Demonstrate:**
1. Check `nameserver 8.8.8.8` inside `/etc/resolv.conf`.
2. Run `dig google.com +short` to show the instant IP response.
3. Run `dig google.com` to highlight the TTL cache countdown number.

---

### 5. EMBEDDED KNOWLEDGE CHECK & SANDBOX LAB
*   **Quiz Question:** A clear multiple-choice question testing `/etc/hosts` vs `/etc/resolv.conf` priority or DNS caching.
*   **AI Explainer:** Simple 2-sentence explanation of why the answer is correct.
*   **Killercoda Lab Challenge:** A step-by-step practical exercise for students in an embedded browser terminal.
