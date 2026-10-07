[⬅ Step 0](00-tools-to-install.md) · [🏠 Home](../README.md) · **Step 1 of 9** · [Next ➡ Step 2: Install the tools](02-install-the-tools.md)

# Step 1: Install WSL + Ubuntu

**Goal:** have Linux (Ubuntu 24.04) running on your Windows PC.
**Time:** 15-30 minutes (one time only).
**Already have Ubuntu in WSL?** Open it, run `lsb_release -a`. If it shows 22.04 or 24.04, skip to [part 3](#3-install-vs-code--wsl-extension).

> **Why WSL?** All the course tools are Linux tools. Running them in Windows directly
> causes terminal bugs, so everything runs inside Ubuntu.

---

## 1. Install WSL with Ubuntu

1. Click **Start**, type `PowerShell`, right-click **Windows PowerShell** → **Run as administrator** → **Yes**.
2. Copy this command, paste it into PowerShell (right-click pastes), press **Enter**:

   ```powershell
   wsl --install -d Ubuntu-24.04
   ```

3. When it finishes, **restart your PC** if it asks you to.

## 2. Create your Ubuntu user

1. After the restart, an **Ubuntu** window opens by itself. If it does not, click **Start** → type `Ubuntu` → open **Ubuntu 24.04**.
2. It asks for a **username**: type a short lowercase name (example: `sagidi`) → **Enter**.
3. It asks for a **password**: type it → **Enter** → type it again → **Enter**.
   > Nothing shows on screen while you type a password. That is normal in Linux.
   > Write the password down: Ubuntu asks for it when installing things.
4. Update Ubuntu (copy, paste with **right-click**, **Enter**, then type your password):

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

5. Check the version:

   ```bash
   lsb_release -a
   ```

   You should see `Ubuntu 24.04` (22.04 also works).

## 3. Install VS Code + WSL extension

VS Code is the easiest way to open and edit your module files.

1. Download and install VS Code: [code.visualstudio.com](https://code.visualstudio.com/) (keep all default options).
2. Open VS Code → click the **Extensions** icon on the left (four squares) → search **WSL** → install **WSL** by Microsoft. Direct link: [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl).
3. Test it: in the Ubuntu window type:

   ```bash
   code .
   ```

   VS Code opens, connected to Ubuntu (bottom-left corner shows **WSL: Ubuntu-24.04**).

## 4. (Optional) Windows Terminal

On Windows 11 it is already installed. On Windows 10 install it from the [Microsoft Store](https://aka.ms/terminal).
In Windows Terminal, click the **⌄** arrow next to the tab → **Ubuntu 24.04** to open Ubuntu.

---

## Good habits from now on

- **Copy/paste in the Ubuntu window:** select text to copy. **Right-click** (or **Ctrl+Shift+V**) to paste.
- **Always work in your Linux home folder** (`~`), **not** in `/mnt/c/...`. Files on the C: drive are slow and cause permission problems in WSL.
- **See Ubuntu files in Windows Explorer:** in Ubuntu type `explorer.exe .` (the dot means "this folder").

---

## ✅ Done when

- The Ubuntu window opens and `lsb_release -a` shows Ubuntu 24.04 (or 22.04).
- `code .` opens VS Code connected to WSL.

## ❌ If something goes wrong

| Problem | Fix |
|---------|-----|
| `Please enable the Virtual Machine Platform` / `virtualization` error | Restart the PC, open the BIOS/UEFI settings and turn on **Virtualization** (Intel VT-x / AMD-V). Then run `wsl --install -d Ubuntu-24.04` again |
| `wsl` command not found | Update Windows (Settings → Windows Update), then try again |
| Ubuntu window closes straight away | In PowerShell (admin): `wsl --update`, then restart |
| `code .` does nothing | Close and reopen the Ubuntu window after installing VS Code |

More fixes: [Troubleshooting](reference/troubleshooting.md#step-1-wsl).

[⬅ Step 0](00-tools-to-install.md) · [🏠 Home](../README.md) · **Step 1 of 9** · [Next ➡ Step 2: Install the tools](02-install-the-tools.md)
