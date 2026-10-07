[🏠 Home](../../README.md) · Reference

# module.yaml reference

The full working example is [Module 1.2's module.yaml](../../modules/module-1.2-dns-ttl-caching/module.yaml).
Copy from it when in doubt. `./build.sh X.Y --check` tells you exactly which line is wrong.

## YAML in 60 seconds

- Indentation (spaces, **never tabs**) shows what belongs to what. Keep the same indentation as the lines around.
- `key: "value"`: put text in **double quotes**. If the text contains `"`, use single quotes `'...'` instead.
- A list item starts with `- `.
- `key: |` followed by indented lines = multi-line text (line breaks are kept).
- `# ...` is a comment (ignored), except inside a `|` block, where it is normal text.

## Text markup (slides only, never in narration)

| Write | Shows as |
|-------|----------|
| `**Fix:**` | **bold** |
| `` `dig google.com` `` | code style |
| `[red]text[/red]` · `[orange]…[/orange]` · `[green]…[/green]` · `[blue]…[/blue]` · `[muted]…[/muted]` | coloured text |
| new line in a `\|` block, or `\n` in quotes | line break |

## Top-level sections

```yaml
module:      # title-slide info + module number          (required)
scenes:      # the 12 scenes: slide and/or demo + narration (required)
quiz:        # 1-5 questions (3 recommended)               (required)
lab:         # Killercoda hands-on lab                     (required)
pronounce:   # optional, module-only pronunciation fixes (same as in course.yaml)
```

### `module`

```yaml
module:
  number: "1.2"                          # quoted
  label: "LINUX NETWORKING & LOGGING"    # small blue line above the title
  title: "Linux DNS & TTL Caching Architecture"
  subtitle: "How Hostnames Translate to IP Addresses..."
  info:                                  # 1-3 boxes at the bottom of the title slide
    - heading: "Target Infrastructure:"
      text: "Splunk Indexer Clusters & ClickHouse Log Engines"
  next:                                  # shown on the last slide
    number: "1.3"
    title: "Linux System Logging (/var/log & journalctl)"
```

### A scene

```yaml
  - id: demo-dig                 # lowercase-with-dashes, unique
    slide: { ... }               # picture for the PDF (and the video, if there is no demo)
    demo: { ... }                # optional: terminal recording used in the video instead of the slide
    narration: |                 # plain spoken English: no markup, no symbols
      When you run dig google.com, you will see...
    hold: 5                      # optional: minimum seconds on screen (e.g. a silent scene)
```

## Slide types

Every type except `title` needs `number`, `title` and `subtitle`:

```yaml
    slide:
      type: table
      number: "1.2.2"
      title: "ENTERPRISE OPERATIONS: DNS in Splunk & ClickHouse"
      subtitle: "Connecting DNS mechanics directly to log ingestion reliability..."
```

| `type` | Extra fields | Used for |
|--------|--------------|----------|
| `title` | none (uses the `module` section) | Scene 1 |
| `two_columns` | `left:` and `right:`, each with `heading`, `color`, and any of `example`, `text`, `bullets`, `code` | Comparisons, two key files |
| `table` | `columns` (2-4), `rows` (1-6, one cell per column), optional `widths` (e.g. `[20, 50, 30]`) | Impact, steps, outage framework |
| `diagram` | `heading`, `lines` (spacing kept, ASCII arrows like `──>` work), `takeaways` (0-3) | Flow diagram |
| `panel` | `heading`, `text`, `subheading`, `bullets` | One deep-dive idea |
| `terminal` | `panels` (1-2, each `heading`, `color`, `lines`), `takeaways`, `note` | Expected command output |
| `quiz` | `question: 1` (which quiz question to show) | Knowledge check |
| `lab` | `steps` (list of short lines), `next_text` | Lab + next module preview |

`color` can be `blue`, `red`, `orange`, `green` or `muted`.

## Demo (terminal recording)

```yaml
    demo:
      setup: |                         # hidden: runs before recording starts (not shown)
        printf 'nameserver 8.8.8.8\n' > /tmp/clean_resolv.conf
      commands:
        - comment: "# Step 1: Inspect the resolver"   # optional, typed first, must start with #
          run: "cat /tmp/clean_resolv.conf"           # typed and run for real
          wait: 5                                     # seconds to show the output (1-20)
```

The look and speed (theme, font, typing speed) come from `course.yaml` → `terminal`.
**Rules:** no `sudo`, nothing interactive (`nano`, `less`, `top`), nothing that runs forever (`ping` needs `-c 3`,
`journalctl` needs `--no-pager`). The check stops the build if a command breaks these rules.

## Quiz

```yaml
quiz:
  - topic: "Priority Resolution Order"       # optional, shown on the quiz slide
    question: "Which file does Linux check first...?"
    options: ["/etc/resolv.conf", "/etc/hosts", "/etc/bind/named.conf"]
    answer: B                                 # letter of the correct option
    explanation: "Linux checks /etc/hosts before..."
    tip: "Add critical indexer hostnames to /etc/hosts..."   # optional
```

## Lab (Killercoda)

```yaml
lab:
  title: "DNS & TTL Caching Lab"
  image: ubuntu                     # Killercoda environment
  setup: |                          # optional: runs in the background when the lab starts
    apt-get install -y -qq dnsutils
  intro: "In this lab you will..."
  steps:
    - title: "Add a static mapping in /etc/hosts"
      text: "Map the name `splunk-master.local` to `127.0.0.1`..."
      commands: ["echo '127.0.0.1 splunk-master.local' >> /etc/hosts"]   # click-to-run in the lab
      verify: "grep -q 'splunk-master.local' /etc/hosts"               # optional: must succeed to pass
  finish: "Well done! ..."
```

[🏠 Home](../../README.md)
