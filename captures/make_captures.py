import os
from PIL import Image, ImageDraw, ImageFont

CAP = "captures"
FONT = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)
TITLE_FONT = ImageFont.truetype(r"C:\Windows\Fonts\consolab.ttf", 16)

BG = (30, 30, 30)
FG = (220, 220, 220)
BAR = (60, 60, 60)


def render(title, lines, out):
    pad = 14
    line_h = 22
    width = 900
    height = 34 + pad * 2 + line_h * len(lines)
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width, 34], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([12 + i * 22, 11, 12 + i * 22 + 12, 23], fill=c)
    d.text((pad, 9), title, font=TITLE_FONT, fill=FG)
    y = 34 + pad
    for ln in lines:
        d.text((pad, y), ln, font=FONT, fill=FG)
        y += line_h
    img.save(out)


def read(fn):
    with open(os.path.join(CAP, fn), encoding="utf-8", errors="replace") as f:
        return f.read().rstrip("\n").replace("\r", "").split("\n")


jobs = [
    ("prereq.txt", "PowerShell  -  versions des outils", "capture_01_prereq.png"),
    ("tree.txt", "Arborescence du projet devops-tp1", "capture_02_tree.png"),
    ("pytest_output.txt", "PowerShell  -  pytest -v", "capture_03_pytest.png"),
    ("git_log.txt", "Git  -  git log --oneline", "capture_04_git_log.png"),
    ("docker_images.txt", "PowerShell  -  docker images devops-tp1", "capture_05_docker_images.png"),
    ("docker_ps.txt", "PowerShell  -  docker ps", "capture_06_docker_ps.png"),
    ("endpoint_root.txt", "Invoke-RestMethod  http://127.0.0.1:5000/", "capture_07_endpoint_root.png"),
    ("endpoint_hello.txt", "Invoke-RestMethod  http://127.0.0.1:5000/hello/EMSI", "capture_08_endpoint_hello.png"),
    ("ci.txt", "GitHub Actions  -  .github/workflows/ci.yml", "capture_09_ci.png"),
]

for src, title, out in jobs:
    render(title, read(src), os.path.join(CAP, out))
    print("wrote", out)