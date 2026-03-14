import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 8))

# Create components
components = [
    {"name": "Video Source", "pos": (0.1, 0.5), "color": "lightblue"},
    {"name": "Encoder\n(H.264/HEVC)", "pos": (0.25, 0.5), "color": "lavender"},
    {"name": "Transmit Buffer\n70% Full", "pos": (0.4, 0.5), "color": "wheat"},
    {"name": "Network\nVariable BW", "pos": (0.55, 0.5), "color": "lightgray"},
    {"name": "Jitter Buffer\n200ms Size", "pos": (0.7, 0.5), "color": "honeydew"},
    {"name": "Decoder", "pos": (0.85, 0.5), "color": "lavender"},
    {"name": "Playback Buffer\n40% Full", "pos": (0.85, 0.3), "color": "wheat"},
    {"name": "Display", "pos": (0.85, 0.1), "color": "lightpink"},
    {"name": "Buffer Monitor\n& Control", "pos": (0.4, 0.2), "color": "seashell"}
]

for comp in components:
    ax.add_patch(patches.Rectangle(
        (comp["pos"][0], comp["pos"][1]), 0.08, 0.08,
        facecolor=comp["color"], edgecolor="black"
    ))
    ax.text(comp["pos"][0]+0.04, comp["pos"][1]+0.1, 
            comp["name"], ha="center", va="center", fontsize=8)

# Add connections
connections = [(0.18,0.54), (0.33,0.54), (0.48,0.54), (0.63,0.54), 
               (0.78,0.54), (0.89,0.46), (0.89,0.34), (0.89,0.18)]
for i in range(len(connections)-1):
    ax.annotate("", xy=connections[i+1], xytext=connections[i],
                arrowprops=dict(arrowstyle="->"))

plt.title("Video Transmission with Buffer Management", fontsize=14)
plt.axis("off")
plt.show()