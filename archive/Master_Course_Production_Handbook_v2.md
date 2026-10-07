# Master Playbook: End-to-End Automated Technical Course Production Engine

Welcome to your complete, zero-guesswork operating manual for creating professional, beginner-friendly technical courses. Every tool, script, prompt, and step from our architecture has been combined into this single, sequential blueprint.

---

## Table of Contents
1. [Overview & Architecture Philosophy](#1-overview--architecture-philosophy)
2. [Prerequisites & System Setup](#2-prerequisites--system-setup)
3. [Required API Keys & Environment Variables](#3-required-api-keys--environment-variables)
4. [Master Directory Structure](#4-master-directory-structure)
5. [The Master Production Workflow (Step-by-Step)](#5-the-master-production-workflow-step-by-step)
   - [Step 1: Module Asset Generation (Master Prompt v2.2)](#step-1-module-asset-generation-master-prompt-v22)
   - [Step 2: Automated Slide Deck Creation (ReportLab PDF)](#step-2-automated-slide-deck-creation-reportlab-pdf)
   - [Step 3: Automated CLI Video Recording (VHS by Charm)](#step-3-automated-cli-video-recording-vhs-by-charm)
   - [Step 4: Automated Voiceover Synthesis (ElevenLabs API)](#step-4-automated-voiceover-synthesis-elevenlabs-api)
   - [Step 5: Automated Video & Audio Stitching (FFmpeg CLI)](#step-5-automated-video--audio-stitching-ffmpeg-cli)
6. [Master One-Click Build Script (`build_module.sh`)](#6-master-one-click-build-script-build_modulesh)
7. [Publishing, LMS & Sandbox Lab Setup](#7-publishing-lms--sandbox-lab-setup)
8. [Module Execution Checklist](#8-module-execution-checklist)

---

## 1. Overview & Architecture Philosophy

This production engine builds high-quality Linux/SRE video courses without manual screen recording, typing errors, or manual video editing. 

### Key Principles
- **Code-as-Video:** Terminal demonstrations are written in `.tape` configuration files and rendered programmatically using VHS by Charm.
- **Beginner-Friendly Language (Directive v2.2):** Technical concepts are explained in plain, direct English. Low-level C functions (like `getaddrinfo()`) are replaced with clear concepts ("how Linux asks for an IP"), and complex taxonomy ("Vector agent load balancing") is replaced with direct operational logic ("how forwarders send logs to Splunk").
- **Dark Slate Visual Standard:** Videos and slides use the **Catppuccin Macchiato** theme (`#1E1E2E` canvas) for maximum readability and a studio-grade aesthetic.
- **Zero-Manual Stitching:** FFmpeg and Python scripts pull voiceovers from ElevenLabs and stitch them to your CLI videos in one command.

---

## 2. Prerequisites & System Setup

All recording and build commands run inside **WSL (Windows Subsystem for Linux - Ubuntu)** to avoid Windows ConPTY terminal bugs.

### WSL Installation Commands
Open PowerShell as Administrator on Windows and execute:

```bash
# 1. Update package list
sudo apt update && sudo apt upgrade -y

# 2. Install FFmpeg, Python3, Pip, and Chromium dependencies
sudo apt install -y python3 python3-pip ffmpeg ttyd \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2t64 pango1.0-tools libcairo2

# 3. Install VHS by Charm in WSL
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
sudo apt update && sudo apt install -y vhs

# 4. Install Python libraries for automated slides and API calls
pip3 install reportlab requests
```

---

## 3. Required API Keys & Environment Variables

You need an API key from **ElevenLabs** for automated audio generation.

### Setting Your API Key in WSL
Add your ElevenLabs API key to your WSL environment so scripts can read it automatically:

```bash
# Open your bash configuration file
nano ~/.bashrc

# Scroll to the bottom and add this line (replace with your actual key):
export ELEVENLABS_API_KEY="your_actual_elevenlabs_api_key_here"

# Save and exit (CTRL+O, ENTER, CTRL+X), then reload:
source ~/.bashrc
```

---

## 4. Master Directory Structure

Keep your course project organized inside a single directory on your drive.

```bash
# Create and enter your course workspace
mkdir -p ~/LinuxCourse/Module_1_2
cd ~/LinuxCourse/Module_1_2
```

Your workspace layout will look like this:
```text
~/LinuxCourse/Module_1_2/
├── linux_course_prompt_template_v2_2.md   # Master Prompt Template
├── generate_slides.py                     # ReportLab 12-Slide PDF Builder
├── dns_v2_cache.tape                      # VHS Automated Terminal Script
├── generate_audio.py                      # ElevenLabs API Voice Synthesizer
├── build_module.sh                        # Master One-Click Build Script
├── dns_v2_cache.mp4                       # Generated Terminal Video
├── dns_narration.mp3                      # Generated Voiceover Audio
└── Module_1_2_Final.mp4                   # Final Published Lesson Video
```

---

## 5. The Master Production Workflow (Step-by-Step)

---

### Step 1: Module Asset Generation (Master Prompt v2.2)

Use this Master Prompt whenever you generate a new course module. Copy and paste it into Gemini to receive the lesson script, slide deck, `.tape` file, and quiz.

#### `linux_course_prompt_template_v2_2.md`
```markdown
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
```

---

### Step 2: Automated Slide Deck Creation (ReportLab PDF)

Run `generate_slides.py` in WSL to generate the 12-slide presentation PDF automatically.

#### `generate_slides.py`
```python
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_filename = "Linux_DNS_and_TTL_Caching_Beginner_Edition.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=landscape(letter),
    rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
)

styles = getSampleStyleSheet()

# Catppuccin Macchiato Inspired Colors
c_navy = colors.HexColor("#0F172A")
c_accent_blue = colors.HexColor("#38BDF8")
c_accent_orange = colors.HexColor("#F43F5E")
c_accent_green = colors.HexColor("#10B981")
c_yellow = colors.HexColor("#F59E0B")
c_text_dark = colors.HexColor("#334155")
c_text_muted = colors.HexColor("#64748B")
c_bg_light = colors.HexColor("#F8FAFC")
c_code_bg = colors.HexColor("#020617")

title_style = ParagraphStyle('SlideTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=c_navy, spaceAfter=6)
subtitle_style = ParagraphStyle('SlideSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=12, leading=16, textColor=c_text_muted, spaceAfter=14)
body_style = ParagraphStyle('SlideBody', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=16, textColor=c_text_dark)
code_style = ParagraphStyle('CodeText', parent=styles['Normal'], fontName='Courier-Bold', fontSize=10, leading=14, textColor=c_accent_blue)
table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.white)
table_cell_style = ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=c_text_dark)

story = []

def make_header(module_num, title, subtitle):
    return [
        Paragraph(f"<font color='#0369A1'><b>MODULE {module_num}</b></font> | {title}", title_style),
        Paragraph(subtitle, subtitle_style),
        Spacer(1, 10)
    ]

# Slide 1: Title
story.append(Paragraph("MODULE 1.2: BEGINNER LINUX NETWORKING", ParagraphStyle('ModuleHeader', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=c_accent_blue)))
story.append(Spacer(1, 15))
story.append(Paragraph("Linux DNS & Caching Made Simple", ParagraphStyle('MainTitle', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=c_navy)))
story.append(Spacer(1, 10))
story.append(Paragraph("How Linux Converts Domain Names into IP Addresses so Forwarders Can Send Logs to Splunk and ClickHouse Servers", ParagraphStyle('MainSub', fontName='Helvetica', fontSize=16, leading=22, textColor=c_text_muted)))
story.append(Spacer(1, 40))

t_title = Table([[
    Paragraph("<b>Goal:</b><br/>Understand how names resolve to IPs", body_style),
    Paragraph("<b>Key Tools:</b><br/><code>/etc/resolv.conf</code>, <code>dig</code>, <code>nslookup</code>", body_style),
    Paragraph("<b>Real Impact:</b><br/>Keep data moving to Splunk without stops", body_style)
]], colWidths=[240, 250, 230])
t_title.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
    ('PADDING', (0,0), (-1,-1), 16),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LINEBELOW', (0,0), (-1,-1), 2, c_accent_blue),
]))
story.append(t_title)
story.append(PageBreak())

# Slide 2: IP vs DNS
story.extend(make_header("1.2.1", "CORE CONCEPTS: IP Address vs. DNS Name", "The two ways computers and humans identify servers on a network."))
c1 = [
    Paragraph("<b>IP ADDRESS (Computer Address)</b>", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=c_accent_blue)),
    Spacer(1, 6),
    Paragraph("<b>Example:</b> <code>142.250.190.46</code>", body_style),
    Spacer(1, 6),
    Paragraph("• The exact numerical street address of a server on the network.<br/>• Used by network cards and routers to deliver data.<br/>• Hard for humans to remember.", body_style)
]
c2 = [
    Paragraph("<b>DNS NAME (Human Label)</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=c_accent_orange)),
    Spacer(1, 6),
    Paragraph("<b>Example:</b> <code>google.com</code>", body_style),
    Spacer(1, 6),
    Paragraph("• The easy-to-remember name we type into a browser or configuration file.<br/>• Must be converted into an IP address before data can travel.<br/>• Translates automatically in the background.", body_style)
]
t_concept = Table([[c1, c2]], colWidths=[355, 355])
t_concept.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), c_bg_light),
    ('BACKGROUND', (1,0), (1,0), c_bg_light),
    ('PADDING', (0,0), (-1,-1), 18),
    ('BOX', (0,0), (0,0), 1, colors.HexColor("#CBD5E1")),
    ('BOX', (1,0), (1,0), 1, colors.HexColor("#CBD5E1")),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t_concept)
story.append(PageBreak())

# Slide 3: Real World Impact
story.extend(make_header("1.2.2", "REAL WORLD IMPACT: Sending Logs to Splunk", "Why DNS resolution is critical for keeping server log pipelines working."))
pipe_data = [
    [Paragraph("<b>Log Task</b>", table_header_style), Paragraph("<b>How DNS Works Here</b>", table_header_style), Paragraph("<b>What Breaks If DNS Fails</b>", table_header_style)],
    [
        Paragraph("<b>1. Sending Logs to Splunk</b>", table_cell_style),
        Paragraph("Forwarders look up the DNS name of the Splunk server to know where to send log data.", table_cell_style),
        Paragraph("<font color='#F43F5E'><b>Pipeline Stopped:</b></font><br/>Forwarders cannot find the server. Logs get stuck and fill up local hard drive space.", table_cell_style)
    ],
    [
        Paragraph("<b>2. ClickHouse Analytics</b>", table_cell_style),
        Paragraph("ClickHouse converts IP addresses into server names so humans can read security logs easily.", table_cell_style),
        Paragraph("<font color='#F59E0B'><b>Slow Dashboards:</b></font><br/>Reports take seconds instead of milliseconds to load.", table_cell_style)
    ],
    [
        Paragraph("<b>3. Server Failover</b>", table_cell_style),
        Paragraph("When a primary server goes down, DNS points the server name to a new backup IP.", table_cell_style),
        Paragraph("<font color='#F43F5E'><b>Lost Connection:</b></font><br/>Logs keep going to the old dead IP address if DNS is not updated.", table_cell_style)
    ]
]
t_pipe = Table(pipe_data, colWidths=[150, 370, 200])
t_pipe.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), c_navy),
    ('PADDING', (0,0), (-1,-1), 10),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('BACKGROUND', (0,1), (-1,1), c_bg_light),
    ('BACKGROUND', (0,3), (-1,3), c_bg_light),
]))
story.append(t_pipe)
story.append(PageBreak())

# Slide 4: Simple Diagram
story.extend(make_header("1.2.3", "THE DNS FLOW DIAGRAM", "How your computer asks Google DNS (8.8.8.8) for an IP address."))
diag_box = [
    Paragraph("<b>MODULE 1: LINUX DNS & TTL CACHING ARCHITECTURE</b>", ParagraphStyle('DiagH', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=c_accent_blue)),
    Spacer(1, 10),
    Paragraph("<code>[ CLIENT PC ] ─────────────&gt; [ GOOGLE PUBLIC DNS ] ─────────────&gt; [ TARGET SERVER ]</code>", code_style),
    Paragraph("<code> /etc/resolv.conf               IP: 8.8.8.8                            google.com</code>", code_style),
    Paragraph("<code> nameserver 8.8.8.8             TTL Cache: Active                      142.250.190.46</code>", code_style),
    Spacer(1, 15),
    Paragraph("<b>💡 SIMPLE LESSON:</b>", ParagraphStyle('TakeawayH', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_yellow)),
    Spacer(1, 4),
    Paragraph("<b>1. First Time:</b> Computer asks Google DNS (<code>8.8.8.8</code>) -&gt; Gets IP (<code>142.250.190.46</code>) -&gt; Saves it in local memory.<br/><b>2. Next Time:</b> Computer reuses the saved IP instantly without asking Google DNS again.", body_style)
]
t_diag = Table([[diag_box]], colWidths=[720])
t_diag.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
    ('PADDING', (0,0), (-1,-1), 20),
    ('BOX', (0,0), (-1,-1), 2, c_accent_blue),
]))
story.append(t_diag)
story.append(PageBreak())

# Slide 5: 4 Easy Steps
story.extend(make_header("1.2.4", "STEP-BY-STEP: What Happens When You Request a Web Page", "The 4 simple steps Linux takes to find a server address."))
steps_data = [
    [Paragraph("<b>Step</b>", table_header_style), Paragraph("<b>Where Linux Looks</b>", table_header_style), Paragraph("<b>What Happens</b>", table_header_style)],
    [Paragraph("<b>Step 1</b>", table_cell_style), Paragraph("<b>Application Request</b>", table_cell_style), Paragraph("An app or forwarder asks Linux: 'What is the IP address for google.com?'", table_cell_style)],
    [Paragraph("<b>Step 2</b>", table_cell_style), Paragraph("<b>Local Memory & File</b>", table_cell_style), Paragraph("Linux checks its local memory cache and the local static list file (<code>/etc/hosts</code>).", table_cell_style)],
    [Paragraph("<b>Step 3</b>", table_cell_style), Paragraph("<b>Resolver Config</b>", table_cell_style), Paragraph("If not saved locally, Linux reads <code>/etc/resolv.conf</code> to find its network DNS helper (<code>8.8.8.8</code>).", table_cell_style)],
    [Paragraph("<b>Step 4</b>", table_cell_style), Paragraph("<b>DNS Answer</b>", table_cell_style), Paragraph("Google DNS (8.8.8.8) replies with the IP <code>142.250.190.46</code> and a timer telling Linux how long to remember it.", table_cell_style)]
]
t_steps = Table(steps_data, colWidths=[80, 180, 460])
t_steps.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), c_navy),
    ('PADDING', (0,0), (-1,-1), 10),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('BACKGROUND', (0,1), (-1,1), c_bg_light),
    ('BACKGROUND', (0,3), (-1,3), c_bg_light),
]))
story.append(t_steps)
story.append(PageBreak())

# Slide 6: Configuration Files
story.extend(make_header("1.2.5", "THE TWO MAIN FILES: /etc/hosts vs /etc/resolv.conf", "Which file Linux checks first and what each file does."))
c_hosts = [
    Paragraph("<font color='#38BDF8'><b>FIRST CHECK: /etc/hosts</b></font>", ParagraphStyle('PH', fontName='Helvetica-Bold', fontSize=11, leading=14)),
    Spacer(1, 6),
    Paragraph("A simple text file stored directly on your computer containing static IP mappings. Linux always checks this first.", body_style),
    Spacer(1, 8),
    Paragraph("<code>127.0.0.1       localhost<br/>192.168.1.50    splunk-server.local</code>", code_style)
]
c_resolv = [
    Paragraph("<font color='#F43F5E'><b>SECOND CHECK: /etc/resolv.conf</b></font>", ParagraphStyle('PR', fontName='Helvetica-Bold', fontSize=11, leading=14)),
    Spacer(1, 6),
    Paragraph("The configuration file that lists external DNS server IP addresses to ask when a domain name is not in <code>/etc/hosts</code>.", body_style),
    Spacer(1, 8),
    Paragraph("<code>nameserver 8.8.8.8<br/>nameserver 8.8.4.4</code>", code_style)
]
t_config = Table([[c_hosts, c_resolv]], colWidths=[355, 355])
t_config.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), c_bg_light),
    ('BACKGROUND', (1,0), (1,0), c_bg_light),
    ('PADDING', (0,0), (-1,-1), 16),
    ('BOX', (0,0), (0,0), 1, c_accent_blue),
    ('BOX', (1,0), (1,0), 1, c_accent_orange),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t_config)
story.append(PageBreak())

# Slide 7: Caching & TTL
story.extend(make_header("1.2.6", "SAVING TIME: What is TTL & Local Caching?", "How remembering IP addresses keeps your connection fast."))
ttl_info = [
    Paragraph("<b>What is TTL (Time-To-Live)?</b>", ParagraphStyle('TTL_H', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=c_navy)),
    Spacer(1, 6),
    Paragraph("TTL is a timer (in seconds) sent alongside an IP address. It tells your computer exactly how long it can safely save the IP address in memory before asking the DNS server again.", body_style),
    Spacer(1, 10),
    Paragraph("<b>Why Local Caching is Helpful:</b>", ParagraphStyle('TTL_H2', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_navy)),
    Spacer(1, 4),
    Paragraph("• <b>Instant Speed:</b> Saved lookups take 0 milliseconds because no network traffic is sent.<br/>• <b>Less Network Traffic:</b> Prevents sending thousands of repetitive questions across the internet.<br/>• <b>Reliability:</b> If Google DNS stutters briefly, your system keeps working using saved addresses.", body_style)
]
story.append(Table([[ttl_info]], colWidths=[720], style=[
    ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
    ('PADDING', (0,0), (-1,-1), 16),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
]))
story.append(PageBreak())

# Slide 8: CLI Demo 1
story.extend(make_header("1.2.7", "COMMAND DEMO 1: Reading Your DNS Server Settings", "Checking which DNS server your Linux system is configured to use."))
cli_1_content = [
    Paragraph("<b>Terminal Output: Checking /etc/resolv.conf</b>", ParagraphStyle('CLIH1', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_accent_blue)),
    Spacer(1, 6),
    Paragraph("<code>user@linux-lab:~$ <b>cat /etc/resolv.conf</b><br/># DNS configuration file<br/><font color='#F59E0B'>nameserver 8.8.8.8</font><br/>nameserver 8.8.4.4</code>", code_style),
    Spacer(1, 10),
    Paragraph("<b>What This Means:</b><br/>• The line <code>nameserver 8.8.8.8</code> tells Linux to ask Google's Public DNS server whenever it needs to translate a domain name.<br/>• The second line (<code>8.8.4.4</code>) is a backup server if the first one does not answer.", body_style)
]
story.append(Table([[cli_1_content]], colWidths=[720], style=[
    ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
    ('PADDING', (0,0), (-1,-1), 16),
    ('BOX', (0,0), (-1,-1), 1, c_accent_blue),
]))
story.append(PageBreak())

# Slide 9: CLI Demo 2
story.extend(make_header("1.2.8", "COMMAND DEMO 2: Testing Domain Lookup with dig", "Using simple terminal tools to test DNS and check the memory timer."))
dig_box = [
    Paragraph("<b>DIG COMMAND (Shows IP & Cache Timer)</b>", ParagraphStyle('DigH', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=c_accent_blue)),
    Spacer(1, 4),
    Paragraph("<code>$ <b>dig google.com</b><br/>;; ANSWER SECTION:<br/>google.com.    <font color='#F43F5E'><b>299</b></font>   IN   A   142.250.190.46<br/><br/>;; Query time: 14 msec<br/>;; SERVER: 8.8.8.8#53</code>", code_style)
]
ns_box = [
    Paragraph("<b>NSLOOKUP COMMAND (Simple IP Lookup)</b>", ParagraphStyle('NsH', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=c_accent_green)),
    Spacer(1, 4),
    Paragraph("<code>$ <b>nslookup google.com</b><br/>Server:         8.8.8.8<br/>Address:        8.8.8.8#53<br/><br/>Name:   google.com<br/>Address: 142.250.190.46</code>", code_style)
]
t_cli_2 = Table([[dig_box, ns_box]], colWidths=[355, 355])
t_cli_2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
    ('PADDING', (0,0), (-1,-1), 14),
    ('BOX', (0,0), (0,0), 1, c_accent_blue),
    ('BOX', (1,0), (1,0), 1, c_accent_green),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t_cli_2)
story.append(Spacer(1, 10))
story.append(Paragraph("<b>Understanding the Output:</b> The number <code>299</code> is the TTL timer in seconds. It counts down to 0, telling you when Linux will refresh the IP address.", body_style))
story.append(PageBreak())

# Slide 10: Outages & Failure Modes
story.extend(make_header("1.2.9", "COMMON MISTAKES: What Happens When Things Fail?", "Simple causes and clear solutions for DNS issues."))
outage_data = [
    [Paragraph("<b>Setting</b>", table_header_style), Paragraph("<b>Why It Matters</b>", table_header_style), Paragraph("<b>What Happens If Broken</b>", table_header_style)],
    [
        Paragraph("<b>Correct DNS IP in <code>/etc/resolv.conf</code></b>", table_cell_style),
        Paragraph("Tells Linux where to send domain questions.", table_cell_style),
        Paragraph("<font color='#F43F5E'><b>Pipeline Stopped:</b></font><br/>Forwarders cannot find the Splunk server, stopping log delivery.", table_cell_style)
    ],
    [
        Paragraph("<b>Static Mappings in <code>/etc/hosts</code></b>", table_cell_style),
        Paragraph("Provides a backup way to find critical servers without needing network DNS.", table_cell_style),
        Paragraph("<font color='#F59E0B'><b>No Backup:</b></font><br/>If external DNS stutters, log agents lose connection instantly.", table_cell_style)
    ],
    [
        Paragraph("<b>Reasonable Memory Timer (TTL)</b>", table_cell_style),
        Paragraph("Ensures computers update their saved IP addresses when servers move.", table_cell_style),
        Paragraph("<font color='#F43F5E'><b>Sending to Dead IP:</b></font><br/>If timer is set too long, logs go to an offline server IP.", table_cell_style)
    ]
]
t_outage = Table(outage_data, colWidths=[180, 260, 280])
t_outage.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), c_navy),
    ('PADDING', (0,0), (-1,-1), 10),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ('BACKGROUND', (0,1), (-1,1), c_bg_light),
    ('BACKGROUND', (0,3), (-1,3), c_bg_light),
]))
story.append(t_outage)
story.append(PageBreak())

# Slide 11: Quiz & AI
story.extend(make_header("1.2.10", "KNOWLEDGE CHECK: Quiz & AI Explanation", "Test your knowledge on file priority."))
quiz_box = [
    Paragraph("<b>QUIZ QUESTION 1</b>", ParagraphStyle('QH', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_navy)),
    Spacer(1, 4),
    Paragraph("<b>Q:</b> Which file does Linux check FIRST when looking up a server domain name?<br/><br/>A) <code>/etc/resolv.conf</code><br/><b>B) <code>/etc/hosts</code> (CORRECT)</b><br/>C) <code>/var/log/syslog</code>", body_style)
]
ai_box = [
    Paragraph("🤖 <b>AI TUTOR EXPLANATION</b>", ParagraphStyle('AIH', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor("#1E1B4B"))),
    Spacer(1, 4),
    Paragraph("<b>Why Option B is Correct:</b><br/>Linux always checks its local list file (<code>/etc/hosts</code>) first before reaching out to network DNS servers listed in <code>/etc/resolv.conf</code>.<br/><br/><b>Pro-Tip:</b> You can write server names directly into <code>/etc/hosts</code> so log forwarders never have to wait on network DNS queries!", body_style)
]
t_quiz = Table([[quiz_box], [Spacer(1, 10)], [ai_box]], colWidths=[720])
t_quiz.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), c_bg_light),
    ('PADDING', (0,0), (0,0), 12),
    ('BOX', (0,0), (0,0), 1, colors.HexColor("#CBD5E1")),
    ('BACKGROUND', (0,2), (0,2), colors.HexColor("#EEF2FF")),
    ('PADDING', (0,2), (0,2), 12),
    ('BOX', (0,2), (0,2), 1, colors.HexColor("#818CF8")),
]))
story.append(t_quiz)
story.append(PageBreak())

# Slide 12: Next Steps
story.extend(make_header("1.2.11", "PRACTICAL LAB & NEXT LESSON", "Hands-on practice and moving forward."))
lab_box = [
    Paragraph("⚡ <b>PRACTICAL LAB CHALLENGE</b>", ParagraphStyle('LabH', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_accent_green)),
    Spacer(1, 4),
    Paragraph("1. Open the interactive terminal on the right side of your screen.<br/>2. Run <code>cat /etc/resolv.conf</code> to see your current DNS server.<br/>3. Run <code>dig google.com</code> and locate the TTL timer number.<br/>4. Add a line to <code>/etc/hosts</code> mapping <code>127.0.0.1</code> to <code>splunk-server.local</code> and test it using <code>ping</code>.", body_style)
]
next_box = [
    Paragraph("<b>NEXT MODULE: Linux System Logs (/var/log)</b>", ParagraphStyle('NextH', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_navy)),
    Spacer(1, 4),
    Paragraph("Now that you know how computers find server addresses on the network, in the next lesson we will learn where Linux stores system log files (<code>/var/log</code>) and how to view them before sending them to Splunk.", body_style)
]
t_next = Table([[lab_box], [Spacer(1, 10)], [next_box]], colWidths=[720])
t_next.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), colors.HexColor("#ECFDF5")),
    ('PADDING', (0,0), (0,0), 12),
    ('BOX', (0,0), (0,0), 1, c_accent_green),
    ('BACKGROUND', (0,2), (0,2), c_bg_light),
    ('PADDING', (0,2), (0,2), 12),
    ('BOX', (0,2), (0,2), 1, colors.HexColor("#CBD5E1")),
]))
story.append(t_next)

doc.build(story)
print("Slide PDF successfully generated: Linux_DNS_and_TTL_Caching_Beginner_Edition.pdf")
```

---

### Step 3: Automated CLI Video Recording (VHS by Charm)

Save this configuration as `dns_v2_cache.tape`. VHS will launch headless Chromium in WSL and record the terminal in 4K widescreen using **Catppuccin Macchiato**.

#### `dns_v2_cache.tape`
```bash
# VHS Configuration for Professional Dark Theme
Set Theme "Catppuccin Macchiato"
Set FontSize 22
Set Width 1280
Set Height 720

# Educational Pacing Controls
Set TypingSpeed 150ms
Set PlaybackSpeed 0.75

# 1. Silently create a clean resolv.conf file and clear screen
Hide
Type "echo 'nameserver 8.8.8.8' > /tmp/clean_resolv.conf && clear" Enter
Show

# Step 1: Check Local Google DNS Resolver
Type "# Step 1: Inspect local DNS resolver pointing to Google DNS (8.8.8.8)" Sleep 1.5s Enter
Type "cat /tmp/clean_resolv.conf" Sleep 1s Enter
Sleep 5s

# Step 2: Query Domain & Inspect TTL Caching Value
Type "# Step 2: Query domain IP resolution and inspect the TTL cache timer" Sleep 1.5s Enter
Type "dig google.com | grep -A 2 'ANSWER SECTION'" Sleep 1s Enter
Sleep 5s
```

---

### Step 4: Automated Voiceover Synthesis (ElevenLabs API)

Save this Python script as `generate_audio.py`. It sends the plain-English narration script to ElevenLabs and downloads `dns_narration.mp3` automatically.

#### `generate_audio.py`
```python
import os
import requests

# Reads API Key from your WSL environment variable
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" # Standard Voice ID (e.g., Rachel / Adam)

if not ELEVENLABS_API_KEY:
    raise ValueError("ERROR: ELEVENLABS_API_KEY environment variable is missing. Set it using export ELEVENLABS_API_KEY='your_key'")

script_text = (
    "Welcome to Module 1.2: Linux DNS and Caching Made Simple.\n\n"
    "In this lesson, we are going to look at how Linux translates easy-to-read domain names into machine-readable IP addresses, and why this simple step is so critical for keeping your log pipelines running smoothly.\n\n"
    "Every computer on a network has an IP address, like 142.250.190.46. It works just like a physical street address. Routers use it to deliver data quickly across the internet. But humans are terrible at remembering long strings of numbers, so we use domain names like google.com instead. DNS, or the Domain Name System, acts as the automatic phone book that translates human names into computer IP addresses behind the scenes.\n\n"
    "In enterprise log pipelines, DNS is everywhere. For example, log forwarders send security events to a Splunk server name, like splunk-server.local. If your Linux system cannot translate that server name into an IP address, data stops moving instantly. Logs pile up on the local machine, filling up hard drive space until the connection is restored.\n\n"
    "So, how does Linux actually look up an address? It follows four simple steps.\n\n"
    "First, an application or log forwarder asks the operating system for an IP address.\n\n"
    "Second, Linux checks its own local memory cache and its local static overrides file, called /etc/hosts.\n\n"
    "Third, if the address is not found locally, Linux opens the /etc/resolv.conf file to find the IP address of its designated network DNS helper, such as Google's public DNS at 8.8.8.8.\n\n"
    "Fourth, Google DNS returns the correct destination IP address, along with a timer telling Linux how long it can safely remember that address.\n\n"
    "Linux relies on two primary configuration files for this process. The first file is /etc/hosts. This is a simple list stored directly on your machine. Linux always checks /etc/hosts first. If a domain name is listed here, Linux uses that IP immediately without ever reaching out to the network. The second file is /etc/resolv.conf. This file lists external DNS server addresses, like nameserver 8.8.8.8, which Linux uses whenever a domain name isn't found in your local hosts file.\n\n"
    "To save time and network traffic, DNS uses something called TTL, or Time-To-Live. TTL is simply a memory countdown timer sent alongside the IP address. It tells your computer how many seconds it can hold that IP in memory. As long as the timer is active, subsequent connections connect instantly in zero milliseconds, without generating any extra network traffic.\n\n"
    "Let's test this in the terminal. When you run cat /etc/resolv.conf, you can see your active nameserver address. When you run dig google.com, you will see the resolved IP address along with the TTL timer counting down.\n\n"
    "If your DNS configuration breaks, your data pipeline freezes. But by understanding how /etc/hosts and /etc/resolv.conf work together, you can quickly diagnose connection drops and ensure log forwarders deliver data reliably every time.\n\n"
    "Now, head over to the interactive Killercoda terminal on your screen and complete the hands-on exercise. See you in the next lesson!"
)

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY
}

data = {
    "text": script_text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75
    }
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    with open("dns_narration.mp3", "wb") as f:
        f.write(response.content)
    print("Success: Voiceover synthesized and saved to dns_narration.mp3")
else:
    print(f"Error from ElevenLabs API: {response.status_code} - {response.text}")
```

---

### Step 5: Automated Video & Audio Stitching (FFmpeg CLI)

FFmpeg automatically merges your VHS screen recording (`dns_v2_cache.mp4`) with your ElevenLabs voiceover (`dns_narration.mp3`) into a single file without re-encoding lag.

```bash
ffmpeg -y -i dns_v2_cache.mp4 -i dns_narration.mp3 -c:v copy -c:a aac -shortest Module_1_2_Final.mp4
```

---

## 6. Master One-Click Build Script (`build_module.sh`)

Instead of running each command manually, save this master shell script as `build_module.sh`. It executes the entire pipeline automatically in under 60 seconds!

#### `build_module.sh`
```bash
#!/bin/bash
set -e

echo "========================================================"
echo "  STARTING AUTOMATED MODULE PRODUCTION BUILD (MODULE 1.2) "
echo "========================================================"

# Step 1: Build Slide PDF
echo "[1/4] Generating 12-Slide PDF Deck..."
python3 generate_slides.py

# Step 2: Render CLI Video via VHS
echo "[2/4] Rendering 4K Terminal Recording via VHS..."
vhs dns_v2_cache.tape

# Step 3: Synthesize ElevenLabs Audio
echo "[3/4] Synthesizing Studio Voiceover via ElevenLabs API..."
python3 generate_audio.py

# Step 4: Stitch Video & Audio via FFmpeg
echo "[4/4] Stitching Video & Audio via FFmpeg..."
ffmpeg -y -i dns_v2_cache.mp4 -i dns_narration.mp3 -c:v copy -c:a aac Module_1_2_Final.mp4

echo "========================================================"
echo "  BUILD COMPLETE! FINAL LESSON: Module_1_2_Final.mp4"
echo "========================================================"
```

### How to Run the Master Script
```bash
# Make the script executable
chmod +x build_module.sh

# Run the complete build
./build_module.sh
```

---

## 7. Publishing, LMS & Sandbox Lab Setup

Once `Module_1_2_Final.mp4` is built, publish it using this LMS layout:

1. **LMS Platform (LearnWorlds / Thinkific):**
   - Create **Module 1.2: Linux DNS & Caching Made Simple**.
   - Upload `Module_1_2_Final.mp4` as the primary video lesson.
   - Attach `Linux_DNS_and_TTL_Caching_Beginner_Edition.pdf` as the downloadable student slide deck.

2. **Interactive Killercoda Lab:**
   - Create a free account on [Killercoda.com](https://killercoda.com).
   - Set up an Ubuntu 22.04 LTS environment iframe.
   - Configure a 4-step student challenge:
     1. Run `cat /etc/resolv.conf` to identify active nameservers.
     2. Query `dig google.com` and locate the TTL timer.
     3. Add `127.0.0.1 splunk-server.local` to `/etc/hosts`.
     4. Verify static resolution by running `ping -c 1 splunk-server.local`.

3. **Knowledge Check Quiz:**
   - Add the 1-question quiz in LearnWorlds with automated feedback:
     - **Q:** Which file does Linux check FIRST when looking up a server domain name?
     - **Answer:** `/etc/hosts`
     - **AI Feedback:** Linux checks local static file mappings in `/etc/hosts` before making external network calls defined in `/etc/resolv.conf`.

---

## 8. Module Execution Checklist

Use this checklist to track your progress for every course module:

- [ ] **WSL Workspace Created:** `~/LinuxCourse/Module_X` folder exists.
- [ ] **API Key Exported:** `export ELEVENLABS_API_KEY="your_key"` configured in `~/.bashrc`.
- [ ] **Master Prompt v2.2 Applied:** Script, slides, `.tape`, and quiz generated.
- [ ] **Python & VHS Scripts Saved:** `generate_slides.py`, `dns_v2_cache.tape`, and `generate_audio.py` written to disk.
- [ ] **One-Click Build Executed:** `./build_module.sh` completed successfully.
- [ ] **Final Output Verified:** `Module_1_2_Final.mp4` reviewed.
- [ ] **Uploaded & Published:** Video uploaded to LearnWorlds, PDF slide deck attached, and Killercoda lab embedded.
