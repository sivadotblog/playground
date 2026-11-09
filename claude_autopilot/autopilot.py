"""Answer Claude Code prompts while you are away.

Run Claude Code inside tmux, then run this in another terminal:
    python autopilot.py <tmux-session>     (default session name: claude)
Stop it with Ctrl+C when you are back.
"""
import subprocess, sys, time

TARGET = sys.argv[1] if len(sys.argv) > 1 else "claude"
ASK = """Below is the screen of a Claude Code terminal session.
If it is waiting on a permission prompt or a multiple choice question, reply with only the option number to pick.
For permission prompts pick the plain "Yes" option, never "don't ask again".
If it is not waiting on a choice, the action looks destructive, or you are not sure, reply NONE.

"""

def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()

last = handled = ""
while True:
    screen = run("tmux", "capture-pane", "-p", "-t", TARGET)
    if screen == last and screen != handled:  # screen stopped changing, so Claude is waiting
        answer = run("claude", "-p", "--model", "haiku", ASK + screen)
        if answer.isdigit():
            run("tmux", "send-keys", "-t", TARGET, answer)
        print(time.strftime("%H:%M:%S"), answer)
        handled = screen
    last = screen
    time.sleep(5)
