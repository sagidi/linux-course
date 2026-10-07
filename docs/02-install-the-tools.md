[⬅ Step 1](01-install-wsl-ubuntu.md) · [🏠 Home](../README.md) · **Step 2 of 9** · [Next ➡ Step 3: Create accounts & keys](03-create-accounts-and-keys.md)

# Step 2: Download the project and install the tools

**Goal:** this project is in your Ubuntu home folder and every tool is installed and tested.
**Time:** 15-20 minutes (mostly waiting).
**You need:** Step 1 done, your GitHub login.

All commands below go in the **Ubuntu** window. Copy each grey box, paste it (right-click), press **Enter**.

---

## 1. Connect Ubuntu to your GitHub account

1. Install the GitHub command-line tool:

   ```bash
   sudo apt update && sudo apt install -y gh git
   ```

2. Log in:

   ```bash
   gh auth login
   ```

   Answer the questions with the arrow keys + **Enter**:

   | Question | Choose |
   |----------|--------|
   | Where do you use GitHub? | **GitHub.com** |
   | Preferred protocol for Git operations? | **HTTPS** |
   | Authenticate Git with your GitHub credentials? | **Yes** |
   | How would you like to authenticate? | **Login with a web browser** |

   It shows a code like `ABCD-1234`. Press **Enter**. If no browser opens, open
   [github.com/login/device](https://github.com/login/device) yourself, type the code, click **Authorize**.

3. Tell Git your name and email (used to label your saved changes). Use your GitHub email:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your-github-email@example.com"
   ```

## 2. Download this project

```bash
cd ~
gh repo clone sagidi/linux-course
cd ~/linux-course
ls
```

You should see `README.md`, `setup.sh`, `build.sh`, `docs`, `modules` and more.

> **Not seeing `setup.sh`?** The guide may still be on its working branch. Run
> `git checkout claude/dreamy-cori-jepcyv` and `ls` again. (This stops being needed
> once that branch is merged into `main` on GitHub.)

## 3. Run the installer

```bash
./setup.sh
```

- It asks for your **Ubuntu password** (typing is invisible). Type it, press **Enter**.
- It runs 6 stages and prints `OK` for each tool. The first run takes 10-15 minutes.
- At the end it runs a **self-test**, including recording a tiny test video with VHS.

When it works you see:

```
All set! Next step: docs/04-first-test-build.md   (run:  ./build.sh 1.2 --draft)
```

> **You can run `./setup.sh` again at any time.** It skips what is installed and re-tests everything.
> Do this whenever something seems broken.

## 4. Open the project in VS Code

```bash
code ~/linux-course
```

Use the file list on the left to open files. Open `README.md` and press **Ctrl+Shift+V** to read it nicely formatted.

---

## ✅ Done when

`./setup.sh` ends with **All set!** and no `FAIL` lines.

## ❌ If something goes wrong

| What you see | Fix |
|--------------|-----|
| `Permission denied` when running `./setup.sh` | Run `chmod +x *.sh` then `./setup.sh` again |
| `gh: command not found` | Run `sudo apt update && sudo apt install -y gh` |
| `repository not found` when cloning | Run `gh auth login` again and choose the account that owns `sagidi/linux-course` |
| `FAIL VHS could not record a test video` | Open the log: `cat /tmp/vhs-selftest.log`. See [Troubleshooting → VHS](reference/troubleshooting.md#vhs-terminal-recording) |
| A download fails (network) | Run `./setup.sh` again. It continues where it stopped |

More fixes: [Troubleshooting](reference/troubleshooting.md#step-2-setup).

[⬅ Step 1](01-install-wsl-ubuntu.md) · [🏠 Home](../README.md) · **Step 2 of 9** · [Next ➡ Step 3: Create accounts & keys](03-create-accounts-and-keys.md)
