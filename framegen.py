import os
import yaml

FRAMES_DIR = os.path.join(os.path.dirname(__file__), 'frames')

def load_frames(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    if not os.path.isdir(FRAMES_DIR):
        print(f'Frames directory not found: {FRAMES_DIR}')
        return
    for fname in sorted(os.listdir(FRAMES_DIR)):
        if not fname.lower().endswith(('.yml', '.yaml')):
            continue
        data = load_frames(os.path.join(FRAMES_DIR, fname))
        frames = data.get('frames', [])
        for frame in frames:
            name = frame.get('name', 'Unknown')
            prompt = frame.get('prompt', '')
            print(f"[Frame Name: {name}]\nPrompt: {prompt}\n---")

if __name__ == '__main__':
    main()
