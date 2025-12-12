"""Lightweight watcher to rebuild on dataset/template edits (staticjinja-inspired)."""
import subprocess
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

WATCH_PATHS = [Path('data'), Path('templates')]


class RebuildHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.json', '.html')):
            print(f"[watch] Detected change in {event.src_path}. Rebuilding...")
            subprocess.run(['python', 'build.py'], check=False)
            subprocess.run(['python', 'generate_index.py'], check=False)


def main():
    observer = Observer()
    handler = RebuildHandler()
    for path in WATCH_PATHS:
        observer.schedule(handler, str(path), recursive=True)
    observer.start()
    print("[watch] Watching data/ and templates/ for changes. Press Ctrl+C to stop.")
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
