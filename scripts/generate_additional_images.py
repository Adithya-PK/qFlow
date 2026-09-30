import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pptx import Presentation
from pptx.util import Inches, Pt

OUTPUT_DIR = r"C:\Projects\QFlow\presentation_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate QR Poster Mockup Card
def generate_qr_poster_card():
    fig, ax = plt.subplots(figsize=(6, 4.5), dpi=300)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    container = patches.FancyBboxPatch(
        (5, 5), 90, 90,
        boxstyle="round,pad=1,rounding_size=4",
        linewidth=2, edgecolor='#334155', facecolor='#111827', zorder=1
    )
    ax.add_patch(container)

    ax.plot([5, 95], [86, 86], color='#1F2937', lw=1.5)
    ax.text(10, 90, 'QFlow • Physical QR', color='#6366F1', fontsize=10, fontweight='bold')
    ax.text(90, 90, 'Print Ready', color='#10B981', fontsize=9, ha='right')

    ax.text(50, 78, 'Service Center QR Poster', color='#F8FAFC', fontsize=13, fontweight='bold', ha='center')
    ax.text(50, 73, 'Scan with Phone Camera to Join', color='#94A3B8', fontsize=9.5, ha='center')

    # QR Code placeholder frame
    qr_frame = patches.Rectangle((33, 26), 34, 40, facecolor='#FFFFFF', edgecolor='#4F46E5', lw=2, zorder=2)
    ax.add_patch(qr_frame)
    ax.text(50, 46, '[ QR CODE ]', color='#1E1B4B', fontsize=12, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(50, 32, 'http://192.168.1.4:5173', color='#475569', fontsize=7.5, fontfamily='monospace', ha='center', zorder=3)

    btn = patches.FancyBboxPatch(
        (12, 10), 76, 9,
        boxstyle="round,pad=0.5,rounding_size=2.5",
        facecolor='#4F46E5'
    )
    ax.add_patch(btn)
    ax.text(50, 14.5, 'Instant Mobile Web Access', color='#FFFFFF', fontsize=11, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, '09_screen_qr_poster.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0B0F19')
    plt.close()

# Generate Analytics Mockup Card
def generate_analytics_card():
    fig, ax = plt.subplots(figsize=(6, 4.5), dpi=300)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    container = patches.FancyBboxPatch(
        (5, 5), 90, 90,
        boxstyle="round,pad=1,rounding_size=4",
        linewidth=2, edgecolor='#334155', facecolor='#111827', zorder=1
    )
    ax.add_patch(container)

    ax.plot([5, 95], [86, 86], color='#1F2937', lw=1.5)
    ax.text(10, 90, 'QFlow • Analytics', color='#6366F1', fontsize=10, fontweight='bold')
    ax.text(90, 90, 'Live Insights', color='#10B981', fontsize=9, ha='right')

    ax.text(50, 78, 'Performance Metrics', color='#F8FAFC', fontsize=13, fontweight='bold', ha='center')
    ax.text(50, 73, 'Real-Time MongoDB Aggregations', color='#94A3B8', fontsize=9.5, ha='center')

    # Metric mini cards
    def mini_card(x, y, w, h, label, val, color):
        c = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=2", facecolor='#1F2937', edgecolor='#374151', lw=1)
        ax.add_patch(c)
        ax.text(x + w/2, y + h - 5, label, color='#94A3B8', fontsize=8, ha='center')
        ax.text(x + w/2, y + 4, val, color=color, fontsize=12, fontweight='bold', ha='center')

    mini_card(12, 44, 36, 22, 'Tokens Today', '18 Active', '#818CF8')
    mini_card(52, 44, 36, 22, 'Avg Service Time', '8.4 Min', '#34D399')
    mini_card(12, 18, 36, 22, 'Counters Active', '4 Online', '#38BDF8')
    mini_card(52, 18, 36, 22, 'Queue Health', 'Optimal', '#F59E0B')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, '10_screen_analytics.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0B0F19')
    plt.close()

if __name__ == '__main__':
    generate_qr_poster_card()
    generate_analytics_card()
    print("Additional mockups created.")
