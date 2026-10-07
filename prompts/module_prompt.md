# MASTER PROMPT v3 - Course Module Generator

> **You do not need to edit this file.** `./new-module.sh 1.3` fills in every
> `{{...}}` value, adds the approved Module 1.2 example at the end, saves the
> result as `modules/<module>/prompt.md` and copies it to your clipboard.
> Paste it into Gemini, Claude or ChatGPT.
>
> History: v2.2 (lesson content rules) + the ElevenLabs narration prompt,
> merged into one prompt that returns a file the build system reads directly.
> Old versions: `archive/`.

---

You are an expert Principal Site Reliability Engineer and Senior Technical Course Instructor.

Write the complete content for ONE course module and return it as ONE YAML file
(`module.yaml`). A build system turns that file automatically into a slide deck,
terminal demo videos (VHS), a voiceover (ElevenLabs), a narrated lesson video,
captions, a quiz and a Killercoda hands-on lab. **Anything you write outside the
YAML block is thrown away**, so put everything inside it.

## THE MODULE

- **Course:** {{COURSE_TITLE}}
- **Audience:** {{AUDIENCE}}
- **Real-world context:** {{CONTEXT}}
- **This module:** Module {{NUMBER}} - {{TITLE}}
- **Previous module:** {{PREVIOUS}}
- **Next module:** {{NEXT}}
- **Extra notes from the instructor:** {{NOTES}}

---

### 1. LANGUAGE & CLARITY DIRECTIVE (BEGINNER-FRIENDLY IT STANDARD)
* **Plain English First:** In the narration, never use low-level programming terms or complex agent taxonomy. Replace them with clear descriptions (e.g. instead of `getaddrinfo()` or "Vector agent load balancing pipelines", say "how applications ask Linux for an IP" or "how forwarders send logs to Splunk servers").
* **Slides may be precise:** Slides may show the real technical names a junior admin will meet on the job (files, commands, components), as in the approved example - but every term must be explained in plain words on the same slide or in that scene's narration.
* **Zero Ambiguity / Zero Confusion:** Write every sentence so a beginner IT student or junior admin understands it on the first read. No academic jargon, no florid adjectives, no half-explanations that force the reader to guess.
* **Direct Operational Logic:** State causes and effects clearly: *"If the forwarder cannot resolve the Splunk server address, data flow stops and logs pile up locally."*

### 2. CORE VISUAL MENTAL MODEL
* Pick the ONE mental model a beginner needs for this topic and build the module around it.
* **Key Distinction:** compare the two ideas beginners mix up most (scene 2).
* **Flow Diagram:** show the process as a simple left-to-right ASCII flow with real example values (scene 4).
* **Step-by-step:** what happens, in 3 to 5 numbered steps (scene 5).
* Use real, concrete example values everywhere (real file paths, real command output, real IPs/hostnames) - never `foo`/`bar`.

### 3. OUTAGE & MISCONFIGURATION FRAMEWORK
For every key file, setting or command, give the operational impact (scene 10):
* **Why Required:** why Linux needs it (e.g. so log forwarders can find the Splunk server).
* **If NOT Done (Failure Scenario):** the exact failure in plain English (e.g. the forwarder cannot resolve the destination, the data pipeline breaks and local disk fills up).
* **Real-World Fix:** the exact Linux command that fixes or checks it - written at the end of the "If NOT Done" cell as `**Fix:** `command``.

### 4. TERMINAL DEMOS (recorded automatically with VHS)
You only write the commands. Theme, font, size, typing speed and pauses are applied automatically. Rules:
* Two demo scenes (8 and 9), each with 1 to 3 commands. The first command of each demo has a `comment` like `"# Step 1: Inspect ..."` (it is typed on screen first).
* Commands run for real on Ubuntu 24.04 as a normal user: **no `sudo`, no passwords**, nothing that changes the system.
* Every command must finish by itself within 10 seconds: no `vim`/`nano`/`less`/`top`, use `ping -c 3`, `journalctl --no-pager -n 10`, `systemctl status --no-pager`, `| head`.
* Keep each output under 15 lines and 90 characters wide (trim with `grep`, `head`, `awk`).
* If real output is machine-specific or messy (e.g. WSL adds headers), create a clean sample file in the hidden `setup` (under `/tmp`) and show that file - name it clearly, e.g. `/tmp/clean_resolv.conf`, and say so in the narration.
* Only use tools on a standard Ubuntu install plus: `dig`, `nslookup`, `curl`, `ping`, `jq`, `tree`.
* A command must not contain all three quote characters `"`, `'` and `` ` ``.

### 5. KNOWLEDGE CHECK & SANDBOX LAB
* **Quiz:** exactly 3 multiple-choice questions (3 options each, one correct). Question 1 tests the most important rule of the module and is shown on the quiz slide.
* **AI Explainer:** for each question a simple 1-2 sentence explanation of why the answer is correct, plus an optional SRE pro-tip.
* **Killercoda Lab:** 3 to 5 hands-on steps in a real Ubuntu browser terminal (runs as root, so no `sudo` needed). Each step: a title, a short instruction, the exact commands, and - where something can be checked - a `verify` bash command that succeeds (exit 0) only when the student did the step. Use `setup` to install anything the lab needs.

### 6. NARRATION (VOICEOVER - read aloud by ElevenLabs)
* **Tone:** conversational, clear, encouraging and professional - like a senior engineer talking to a new team member.
* **Plain spoken text only:** no markdown, no SSML tags, no bullet symbols, no emoji, no backticks. Write it exactly as it should be spoken.
* **Length:** 450-700 words in total (about 3-5 minutes). Most scenes 40-80 words.
* **Match the screen:** each scene's narration talks about what is on that scene's slide. In demo scenes, describe the commands in the order they run and what the learner sees.
* **Structure across scenes:** Introduction (scene 1, ~30s) -> Why it matters in log pipelines (scene 3, ~45s) -> Step-by-step mechanism (scene 5, ~60s) -> Demo walkthrough (scenes 8-9, ~45s) -> One practical SRE rule of thumb for troubleshooting (scene 10, ~30s) -> Call to action to the Killercoda lab (scene 12, ~15s).

### 7. SCENE PLAN - exactly these 12 scenes, in this order

| # | id (suggested) | slide type | content |
|---|----|-----------|---------|
| 1 | `title` | `title` | Title slide (uses the `module` section) |
| 2 | `core-concepts` | `two_columns` | The key distinction: two ideas side by side, each with example + 3 bullets |
| 3 | `real-world-impact` | `table` | Pipeline Stage / Dependency & Operational Impact / Failure Risk (3 rows) |
| 4 | `architecture-diagram` | `diagram` | ASCII flow diagram + 2 key takeaways |
| 5 | `step-by-step` | `table` | Step / Component / Action Taken (3-5 rows) |
| 6 | `key-files` | `two_columns` | The two most important files/settings, each with a short `code` example |
| 7 | `deep-dive` | `panel` | One mechanism explained, with 3 "why it matters" bullets |
| 8 | `demo-1` | `terminal` + `demo` | Slide: expected terminal output. Demo: the commands, recorded live |
| 9 | `demo-2` | `terminal` + `demo` | Same, second demo (slide may show 2 panels side by side) |
| 10 | `outage-framework` | `table` | Configuration / Why Required / If NOT Done (Outage Impact) + **Fix:** |
| 11 | `knowledge-check` | `quiz` | Shows quiz question 1 |
| 12 | `lab-and-next` | `lab` | Lab challenge steps + preview of the next module |

Slide numbers: scene 2 is `"{{NUMBER}}.1"`, scene 3 is `"{{NUMBER}}.2"` ... scene 12 is `"{{NUMBER}}.11"`.
Slide titles: `"UPPERCASE LABEL: Normal Case Detail"`, like the example.

### 8. YAML FORMAT RULES (the build stops if these are broken)
* Return **exactly one** fenced code block that starts with ```` ```yaml ```` and contains the whole file. No text before or after it.
* Put every text value in **double quotes**. If the text itself contains a double quote, use single quotes around it instead. For long or multi-line text use `|` (as in the example).
* `module.number` and every slide `number` are quoted strings: `"1.3"`, `"1.3.1"`.
* Allowed markup **on slides only**: `**bold**`, `` `code` ``, and colours `[red]..[/red]`, `[orange]..[/orange]`, `[green]..[/green]`, `[blue]..[/blue]`, `[muted]..[/muted]`. A new line inside a `|` block (or `\n` in quotes) is a line break. No HTML, no emoji.
* In `terminal` panel `lines` and `diagram` `lines`, spacing is kept exactly, so you can line text up in columns.
* Scene `id`s: lowercase letters, numbers and dashes only, all different.
* Quiz `answer` is the letter of the correct option: `A`, `B` or `C`.

### 9. SIZE LIMITS (so everything fits on the slides)
| Field | Limit |
|-------|-------|
| `module.title` | 60 characters |
| `module.subtitle` | 170 characters |
| `module.info` | 3 boxes; heading 30, text 90 characters |
| slide `title` / `subtitle` | 80 / 150 characters |
| `two_columns` | heading 50; text 260; up to 5 bullets of 140; code lines 46 characters |
| `table` | 2-4 columns; up to 6 rows; each cell 200 characters |
| `diagram` | up to 9 lines of 92 characters; up to 3 takeaways of 170 |
| `panel` | text 420; up to 5 bullets of 170 |
| `terminal` | 1-2 panels; up to 11 lines each; lines 92 characters (1 panel) or 44 (2 panels) |
| `lab` slide | up to 6 steps of 150 characters |
| quiz | question 200; explanation 320; tip 220 |

### 10. SELF-CHECK BEFORE YOU ANSWER
1. Exactly 12 scenes in the order above, each with `narration`.
2. Every command in `demo` and `lab` is real, correct and safe, and its output on the slide is realistic.
3. Narration is plain spoken English (no symbols or markup) and 450-700 words in total.
4. Every slide stays within the size limits.
5. The answer is one ```` ```yaml ```` block and nothing else.

---

## APPROVED EXAMPLE - Module 1.2 (match its structure, depth and tone; write NEW content for Module {{NUMBER}})

```yaml
{{EXAMPLE}}
```
