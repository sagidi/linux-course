[🏠 Home](../../README.md) · Reference

# Working with Claude (cheaply)

## Let Claude run the commands on your PC (optional)

A Claude session in the cloud cannot reach your PC. To let Claude run `./setup.sh`, `./build.sh` and fix
problems directly on your computer, run Claude Code **inside Ubuntu**, in the project folder:

1. Install Claude Code in Ubuntu: follow [the official setup guide](https://code.claude.com/docs/en/setup).
2. Start it in the project folder, either:
   - `cd ~/linux-course && claude` to work in the terminal, or
   - `cd ~/linux-course && claude remote-control` so the session appears in the **Claude Code app** (phone or desktop) and you can drive it from there.
3. Claude reads [`CLAUDE.md`](../../CLAUDE.md) in this folder automatically, so it already knows how the project works.

## Ask in a way that saves tokens

| Instead of | Say |
|-----------|-----|
| "Make module 1.3" (from scratch, long chat) | "Run `./new-module.sh 1.3`, then write `module.yaml` following `prompts/module_prompt.md`, then run `./build.sh 1.3 --check`." |
| Pasting whole files into the chat | Give the path: "Look at `modules/module-1.3-*/module.yaml`, scene `demo-2`." |
| "It doesn't work" | The command you ran + the exact `ERROR:` lines |
| Re-explaining the project | Nothing: `CLAUDE.md` and these docs explain it |
| Asking for the whole course in one go | One module per chat ([why](why-and-what-changed.md#why-one-complete-module-at-a-time)) |

[🏠 Home](../../README.md)
