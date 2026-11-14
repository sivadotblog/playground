# Claude Autopilot

Answers Claude Code permission prompts and multiple choice questions while you are away. If it is not sure, it does nothing.

## How it works

Every 5 seconds it reads the Claude Code screen from tmux. When the screen stops changing, Claude Code is waiting. The script sends that screen to `claude -p` (Haiku), which replies with an option number or NONE. A number gets typed into the session. NONE does nothing.

It needs no pip packages and no API key. It uses your existing Claude Code login.

## Use

```
tmux new -s claude      # start Claude Code inside this session
claude
```

In another terminal, when you step away:

```
python autopilot.py claude
```

Press Ctrl+C when you are back.

## Notes

- It always picks plain "Yes", never "don't ask again".
- It answers NONE for anything that looks destructive.
- It still approves whatever Haiku judges safe, so only use it in projects where that risk is acceptable.
