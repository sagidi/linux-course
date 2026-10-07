[🏠 Home](../../README.md) · Reference · Optional

# Manual editing with CapCut or Descript (optional)

**You do not need this.** `./build.sh` already lines up slides, terminal demos and voice automatically.
Use this only if you want hand-made extras: zoom-ins, arrows, callouts, music, or a custom intro.

## Get the pieces

After a build, the separate pieces are in `modules/<module>/build/work/`:

| Piece | Where |
|-------|-------|
| Slide images | `work/slides/slide-01.png` ... |
| Terminal clips | `work/demos/<scene-id>.mp4` |
| Voice per scene | `work/audio/<scene-id>-....mp3` (final) or `.wav` (draft) |
| The whole video, already synced | `publish/Module_X_Y_Final.mp4` |

**Easiest:** import the finished `Module_X_Y_Final.mp4` and add your extras on top. The timing is already right.

## Building it by hand: the 3-track timeline

Think of the editor as a sandwich of horizontal tracks:

```
[ Track 3 (top overlay) ]  Instructor photo/avatar ───────────────── (corner, whole lesson)
[ Track 2 (main visual) ]  Slide 1 ─> Slide 2 ─> ... ─> Terminal clip ─> ... ─> Lab slide
[ Track 1 (main audio)  ]  Voiceover (the "master clock") ──────────────────────────────
```

1. **Voice first:** put the narration on Track 1. It sets the timing for everything.
2. **Slides:** put each slide image on Track 2 and stretch it until the narration about it ends.
   When the voice says *"Every computer on a network has an IP address..."*, switch to the IP vs DNS slide, and so on.
3. **Terminal clips:** when the voice says *"Let's test this in the terminal..."*, switch Track 2 to the terminal clip.
   The clips include 5-second pauses after each output, so the screen stays still while the voice explains.
   If a clip is slightly fast or slow, change its speed (e.g. 0.9x or 1.1x) or trim pauses.
4. **Ending:** when the voice says *"head over to the interactive Killercoda terminal..."*, show the lab slide.
5. **Overlay:** put your round photo on Track 3 in a corner.
6. **Captions:** import `Module_X_Y_Captions.srt`, or use the editor's auto-captions.
7. **Export:** 1080p MP4.

[🏠 Home](../../README.md)
