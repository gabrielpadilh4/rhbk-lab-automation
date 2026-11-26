#!/usr/bin/env python3
"""Render the RHBK HA architecture diagram (diagram.png) next to this script.

Regenerate after changing hostnames/IPs/ports:  python3 docs/diagram.py
Requires: Pillow  (pip install Pillow)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

S = 2  # supersample factor for crisp output
W, H = 1700 * S, 620 * S
FONT_DIR = "/usr/share/fonts/liberation-sans-fonts"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size * S)


f_title = font("LiberationSans-Bold.ttf", 15)
f_host = font("LiberationSans-Bold.ttf", 14)
f_body = font("LiberationSans-Regular.ttf", 12)
f_role = font("LiberationSans-Italic.ttf", 12)
f_edge = font("LiberationSans-Regular.ttf", 12)

# palette (fill, border)
GRAY = ("#eceef1", "#5b6775")
BLUE = ("#d6e4ff", "#2f6fdb")
ORANGE = ("#ffe6cc", "#e07b1a")
GREEN = ("#d9f2e0", "#2e9e52")
OUTER = ("#ffffff", "#1f2933")
INK = "#1f2933"

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)


def rr(x1, y1, x2, y2, fill, border, w=2, radius=10):
    d.rounded_rectangle([x1 * S, y1 * S, x2 * S, y2 * S], radius=radius * S,
                        fill=fill, outline=border, width=w * S)


def center_text(cx, y, lines, fills):
    """lines: list of (text, font); fills: list or single color. returns next y."""
    if isinstance(fills, str):
        fills = [fills] * len(lines)
    yy = y
    for (txt, ft), col in zip(lines, fills):
        bb = d.textbbox((0, 0), txt, font=ft)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        d.text((cx * S - tw / 2, yy * S), txt, font=ft, fill=col)
        yy += (th / S) + 7
    return yy


def label(x1, y1, x2, y2, title, color):
    rr(x1, y1, x2, y2, OUTER[0], color[1], w=2)
    bb = d.textbbox((0, 0), title, font=f_title)
    tw = bb[2] - bb[0]
    d.text(((x1 + x2) / 2 * S - tw / 2, (y1 + 8) * S), title, font=f_title, fill=color[1])


def arrow(x1, y1, x2, y2, text=None, above=True):
    d.line([x1 * S, y1 * S, x2 * S, y2 * S], fill=INK, width=2 * S)
    # arrowhead
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    ln = 9
    for deg in (150, -150):
        da = math.radians(deg)
        hx = x2 - ln * math.cos(ang + da)
        hy = y2 - ln * math.sin(ang + da)
        d.line([x2 * S, y2 * S, hx * S, hy * S], fill=INK, width=2 * S)
    if text:
        bb = d.textbbox((0, 0), text, font=f_edge)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ty = my - th / S - 6 if above else my + 4
        # white bg for readability
        d.rectangle([mx * S - tw / 2 - 4, ty * S - 2, mx * S + tw / 2 + 4, ty * S + th + 2],
                    fill="white")
        d.text((mx * S - tw / 2, ty * S), text, font=f_edge, fill=INK)


# ---- User Access ----
label(30, 170, 230, 420, "User Access", GRAY)
rr(55, 250, 205, 350, GRAY[0], GRAY[1], w=2)
center_text(130, 285, [("Web Browsers", f_host), ("/ Clients", f_host)], INK)

# ---- Load Balancing Layer ----
label(300, 120, 540, 470, "Load Balancing Layer", BLUE)
rr(325, 190, 515, 400, BLUE[0], BLUE[1], w=2)
center_text(420, 215, [
    ("httpd.corp.example.com", f_host),
    ("192.168.122.10", f_body),
    ("OS: RHEL 10", f_body),
    ("Role: Apache HTTPD Proxy", f_role),
    ("Port: 443", f_body),
], [BLUE[1], INK, INK, BLUE[1], INK])

# ---- HA RHBK Cluster ----
label(615, 60, 1180, 560, "High Availability RHBK Cluster", ORANGE)
# node 1
rr(650, 110, 940, 290, ORANGE[0], ORANGE[1], w=2)
center_text(795, 128, [
    ("keycloak01.corp.example.com", f_host),
    ("192.168.122.11", f_body),
    ("OS: RHEL 10", f_body),
    ("Role: Active Node 1", f_role),
    ("Ports: 8080, 7800, 57800, 9000", f_body),
], [ORANGE[1], INK, INK, ORANGE[1], INK])
# node 2
rr(855, 330, 1145, 510, ORANGE[0], ORANGE[1], w=2)
center_text(1000, 348, [
    ("keycloak02.corp.example.com", f_host),
    ("192.168.122.12", f_body),
    ("OS: RHEL 10", f_body),
    ("Role: Active Node 2", f_role),
    ("Ports: 8080, 7800, 57800, 9000", f_body),
], [ORANGE[1], INK, INK, ORANGE[1], INK])
# infinispan replication between nodes
arrow(900, 290, 980, 330)
d.multiline_text((700 * S, 305 * S),
                 "Infinispan Replication\nPorts: 7800 / 57800",
                 font=f_edge, fill=INK, spacing=5 * S)

# ---- Data Persistence Layer ----
label(1255, 170, 1670, 420, "Data Persistence Layer", GREEN)
rr(1290, 220, 1635, 380, GREEN[0], GREEN[1], w=2)
center_text(1462, 238, [
    ("postgresql.corp.example.com", f_host),
    ("192.168.122.13", f_body),
    ("OS: RHEL 10", f_body),
    ("Role: Database Backend", f_role),
    ("Port: 5432", f_body),
], [GREEN[1], INK, INK, GREEN[1], INK])

# ---- edges between layers ----
arrow(205, 300, 325, 300, "HTTPS:443")
arrow(515, 250, 650, 200, "Proxy Request:8080")
arrow(515, 320, 855, 420, "Proxy Request:8080", above=False)
arrow(940, 180, 1290, 260, "JDBC:5432")
arrow(1145, 420, 1290, 340, "JDBC:5432", above=False)

# downscale for anti-aliasing
img = img.resize((W // S, H // S), Image.LANCZOS)
out = os.path.join(HERE, "diagram.png")
img.save(out)
print("wrote", out, img.size)
