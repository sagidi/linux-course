# Master Prompt Template: ElevenLabs Technical Narration Script Generator (v1)

> Saved from the "Pro Linux Course Creation Guide" chat so nothing is lost.
> Its rules now live in section 6 of `prompts/module_prompt.md`, which writes the
> narration together with the slides, so you no longer need to run this separately.

You are an expert Technical Course Scriptwriter and Senior Site Reliability Engineer.
Write a complete, plain-English voiceover narration script for [INSERT MODULE NAME, e.g., Module 1.3: Linux System Logs (/var/log & journalctl)].

## 1. LANGUAGE & CLARITY DIRECTIVES

* **Target Audience:** Beginner IT students, junior admins, and aspiring SREs.
* **Tone:** Conversational, clear, encouraging, and highly professional.
* **Plain-English First:** Eliminate low-level C functions, academic jargon, or overly complex agent taxonomy. Replace them with plain concepts (e.g., "how Linux saves log files" instead of "systemd-journald memory allocation buffers").
* **Zero Ambiguity:** Write every sentence so it can be understood immediately on a single listen.
* **No Formatting Tags in Script Text:** Do NOT include SSML tags, markdown formatting, or bullet points in the actual spoken text output so it can be pasted directly into ElevenLabs.

## 2. SCRIPT STRUCTURE & PACING (3 TO 4 MINUTES TOTAL)

1. **Introduction (30s):** Hook the learner, state the module title, and explain the main goal in simple terms.
2. **The "Why It Matters" Real-World Link (45s):** Connect the concept directly to log pipelines (e.g., Splunk / ClickHouse data flow or system outages).
3. **Step-by-Step Mechanism Breakdown (60s):** Walk through how the Linux tool or file works in 3 to 4 clear, sequential steps.
4. **CLI Demo Walkthrough (45s):** Explain what the learner is seeing on screen during the VHS terminal video (e.g., what `cat /var/log/syslog` or `journalctl -u` outputs).
5. **Outage Avoidance & Practical Tip (30s):** Provide one practical SRE rule of thumb for troubleshooting.
6. **Outro & Call to Action (15s):** Direct the student to the interactive Killercoda terminal lab exercise.

## 3. OUTPUT DELIVERABLE

Provide the finalized script inside a clean text box ready for copy-pasting into ElevenLabs.

---

**Voice settings used with this script:** conversational, clear, confident voice (e.g. Adam, Rachel or Charlie) · Speed 1.0x · Stability 50% · Clarity/Similarity 75%.
