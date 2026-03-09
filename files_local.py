from pathlib import Path

# Folders to exclude
EXCLUDE_DIRS = {".git", ".claude", ".vscode"}

# Tree drawing characters
TEE = "├── "
ELBOW = "└── "
PIPE = "│   "
SPACE = "    "

def save_tree(root: Path, f, prefix: str = ""):
    try:
        entries = sorted(
            [p for p in root.iterdir() if p.name not in EXCLUDE_DIRS],
            key=lambda p: (not p.is_dir(), p.name.lower())
        )
    except PermissionError:
        f.write(prefix + "[Permission denied]\n")
        return

    for i, p in enumerate(entries):
        is_last = (i == len(entries) - 1)
        connector = ELBOW if is_last else TEE
        f.write(prefix + connector + p.name + "\n")

        if p.is_dir():
            extension = SPACE if is_last else PIPE
            save_tree(p, f, prefix + extension)

if __name__ == "__main__":
    root = Path(".").resolve()
    out_path = (Path.cwd() / "files_local.txt").resolve()

    # utf-8-sig ensures Windows Notepad displays the file correctly
    with open(out_path, "w", encoding="utf-8-sig", errors="replace", newline="\n") as f:
        f.write(f"Directory tree for: {root}\n\n")
        save_tree(root, f)

    print(f"Wrote: {out_path}")
