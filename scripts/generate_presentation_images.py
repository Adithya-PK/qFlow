import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Projects\QFlow\presentation_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. USE CASE DIAGRAM (Slide 05)
# -----------------------------------------------------------------------------
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # System Boundary Box
    system_box = patches.FancyBboxPatch(
        (22, 5), 56, 88,
        boxstyle="round,pad=1.5,rounding_size=3",
        linewidth=2, edgecolor='#38BDF8', facecolor='#1E293B', zorder=1
    )
    ax.add_patch(system_box)

    # Title
    ax.text(50, 88, 'QFlow System Boundary', color='#F8FAFC', fontsize=16, fontweight='bold', ha='center')
    ax.text(50, 84, 'Smart Token & Queue Management System', color='#94A3B8', fontsize=11, ha='center')

    # Actors (Stick figures & Labels)
    # Actor 1: Customer (Left)
    ax.scatter(10, 60, s=280, color='#818CF8', zorder=5) # Head
    ax.plot([10, 10], [53, 40], color='#818CF8', lw=3, zorder=5) # Body
    ax.plot([4, 16], [48, 48], color='#818CF8', lw=3, zorder=5) # Arms
    ax.plot([10, 5], [40, 28], color='#818CF8', lw=3, zorder=5) # Left leg
    ax.plot([10, 15], [40, 28], color='#818CF8', lw=3, zorder=5) # Right leg
    ax.text(10, 22, 'Customer\n(Mobile Device)', color='#E0E7FF', fontsize=12, fontweight='bold', ha='center')

    # Actor 2: Staff / Operator (Right Top)
    ax.scatter(90, 68, s=240, color='#34D399', zorder=5)
    ax.plot([90, 90], [62, 52], color='#34D399', lw=3, zorder=5)
    ax.plot([85, 95], [58, 58], color='#34D399', lw=3, zorder=5)
    ax.plot([90, 86], [52, 43], color='#34D399', lw=3, zorder=5)
    ax.plot([90, 94], [52, 43], color='#34D399', lw=3, zorder=5)
    ax.text(90, 37, 'Staff Operator\n(Counter Terminal)', color='#D1FAE5', fontsize=11, fontweight='bold', ha='center')

    # Actor 3: System Admin (Right Bottom)
    ax.scatter(90, 24, s=240, color='#FBBF24', zorder=5)
    ax.plot([90, 90], [18, 9], color='#FBBF24', lw=3, zorder=5)
    ax.plot([85, 95], [14, 14], color='#FBBF24', lw=3, zorder=5)
    ax.plot([90, 86], [9, 2], color='#FBBF24', lw=3, zorder=5)
    ax.plot([90, 94], [9, 2], color='#FBBF24', lw=3, zorder=5)
    ax.text(90, -3, 'System Admin\n(Management)', color='#FEF3C7', fontsize=11, fontweight='bold', ha='center')

    # Use Cases (Ovals in center)
    use_cases = [
        ("Scan Physical QR Code", 73, '#6366F1'),
        ("Register & Generate Token", 61, '#6366F1'),
        ("Track Live Queue & AI Wait Time", 49, '#6366F1'),
        ("Receive 'Your Turn' Live Alert", 37, '#6366F1'),
        ("Call Next / Start / Complete Token", 67, '#059669'),
        ("Skip / Transfer Token", 55, '#059669'),
        ("Manage Counters & Services", 25, '#D97706'),
        ("View Real-Time Analytics & Logs", 13, '#D97706'),
    ]

    # Draw use case bubbles
    for text, y, col in use_cases:
        oval = patches.FancyBboxPatch(
            (30, y - 3.2), 40, 6.4,
            boxstyle="round,pad=0.5,rounding_size=3",
            linewidth=1.5, edgecolor=col, facecolor='#334155', zorder=2
        )
        ax.add_patch(oval)
        ax.text(50, y, text, color='#F8FAFC', fontsize=10.5, fontweight='semibold', ha='center', va='center', zorder=3)

    # Customer Connections (Left to use cases 0, 1, 2, 3)
    for idx in [0, 1, 2, 3]:
        _, y, _ = use_cases[idx]
        ax.annotate('', xy=(30, y), xytext=(15, 48),
                    arrowprops=dict(arrowstyle='->', color='#818CF8', lw=1.5, ls='--'))

    # Staff Connections (Right to use cases 4, 5, 7)
    for idx in [4, 5]:
        _, y, _ = use_cases[idx]
        ax.annotate('', xy=(70, y), xytext=(85, 58),
                    arrowprops=dict(arrowstyle='->', color='#34D399', lw=1.5, ls='--'))

    # Admin Connections (Right to use cases 6, 7)
    for idx in [6, 7]:
        _, y, _ = use_cases[idx]
        ax.annotate('', xy=(70, y), xytext=(85, 14),
                    arrowprops=dict(arrowstyle='->', color='#FBBF24', lw=1.5, ls='--'))

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, '01_use_case_diagram.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0F172A')
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 2. ER DIAGRAM / DATABASE DESIGN (Slide 06)
# -----------------------------------------------------------------------------
def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.8), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#0B132B')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Header Title & Subtitle (Clear Top Zone: y = 92 to 98)
    ax.text(50, 96.5, 'QFlow — MongoDB Document Schema (ER Diagram)', color='#F8FAFC', fontsize=18, fontweight='bold', ha='center')
    ax.text(50, 93, 'Mongoose Schema Models, References & Relationship Cardinality', color='#94A3B8', fontsize=11, ha='center')

    def draw_table(x, y, w, h, title, fields, border_col, header_col):
        # Container Box
        card = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.6,rounding_size=1.5",
            linewidth=2, edgecolor=border_col, facecolor='#1C2541', zorder=3
        )
        ax.add_patch(card)
        
        # Header Banner
        header = patches.Rectangle((x, y + h - 5.2), w, 5.2, facecolor=header_col, zorder=4)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 2.6, title, color='#FFFFFF', fontsize=11.5, fontweight='bold', ha='center', va='center', zorder=5)
        
        # Fields
        cur_y = y + h - 8.5
        for field, ftype in fields:
            is_pk = '(PK)' in field
            is_fk = '(FK)' in field
            name_col = '#38BDF8' if is_pk else ('#FCD34D' if is_fk else '#E2E8F0')
            ax.text(x + 1.8, cur_y, field, color=name_col, fontsize=9.5, fontweight='bold' if (is_pk or is_fk) else 'medium', zorder=5)
            ax.text(x + w - 1.8, cur_y, ftype, color='#94A3B8', fontsize=9, fontfamily='monospace', ha='right', zorder=5)
            cur_y -= 3.5

    # 1. USER (Top Left: y=46 to 78)
    user_fields = [
        ("_id (PK)", "ObjectId"),
        ("name", "String"),
        ("email", "String (Unique)"),
        ("password", "String (Bcrypt)"),
        ("role", "'admin' | 'staff'"),
        ("createdAt", "Date"),
    ]
    draw_table(4, 46, 27, 32, "User (Collection)", user_fields, '#818CF8', '#4338CA')

    # 2. SERVICE (Bottom Left: y=8 to 40)
    service_fields = [
        ("_id (PK)", "ObjectId"),
        ("name", "String (Unique)"),
        ("code", "String (AC, PAY..)"),
        ("averageDuration", "Number (min)"),
        ("active", "Boolean"),
        ("description", "String"),
    ]
    draw_table(4, 8, 27, 32, "Service (Collection)", service_fields, '#FBBF24', '#B45309')

    # 3. TOKEN (Center Core: y=8 to 78)
    token_fields = [
        ("_id (PK)", "ObjectId"),
        ("tokenNumber", "String (Unique A101)"),
        ("customerName", "String"),
        ("phone", "String (10-digit)"),
        ("service", "String (Indexed)"),
        ("status", "Enum (6 States)"),
        ("counterId (FK)", "Ref -> Counter"),
        ("predictedDuration", "Number (AI min)"),
        ("estimatedWait", "Number (AI min)"),
        ("actualDuration", "Number (min)"),
        ("createdAt / calledAt", "Date"),
        ("startedAt / completedAt", "Date"),
        ("transferHistory", "[ObjectId]"),
    ]
    draw_table(36.5, 8, 28, 70, "Token (Core Collection)", token_fields, '#34D399', '#047857')

    # 4. COUNTER (Right Top: y=32 to 78)
    counter_fields = [
        ("_id (PK)", "ObjectId"),
        ("counterNumber", "Number (Unique)"),
        ("staffName", "String"),
        ("status", "Enum (AVAILABLE..)"),
        ("currentTokenId (FK)", "Ref -> Token"),
        ("servicesSupported", "[String]"),
        ("isActive", "Boolean"),
        ("updatedAt", "Date"),
    ]
    draw_table(69, 32, 27, 46, "Counter (Collection)", counter_fields, '#38BDF8', '#0369A1')

    # -------------------------------------------------------------------------
    # NON-OVERLAPPING RELATIONSHIP CONNECTORS & BADGES
    # -------------------------------------------------------------------------

    # 1. User -> Counter (Staff Operates Counter) - Distinct Arch in clear band y=78 to 88
    arch_path = patches.FancyArrowPatch(
        (17.5, 78), (82.5, 78),
        connectionstyle="arc3,rad=-0.18",
        arrowstyle="-|>", mutation_scale=18,
        linestyle=(0, (5, 4)), linewidth=2.5, color='#A5B4FC', zorder=6
    )
    ax.add_patch(arch_path)
    
    # Badge for User -> Counter (centered at peak y=84)
    user_ctr_badge = patches.FancyBboxPatch(
        (36, 82.5), 29, 4.2,
        boxstyle="round,pad=0.3,rounding_size=1",
        facecolor='#1E1B4B', edgecolor='#818CF8', linewidth=1.5, zorder=7
    )
    ax.add_patch(user_ctr_badge)
    ax.text(50.5, 84.6, "Staff Authenticates & Operates Counter", color='#C7D2FE', fontsize=9.5, fontweight='bold', ha='center', va='center', zorder=8)

    # 2. Token <-> Counter (Assigned Counter & Active Serving) - Right Horizontal Bridge
    ax.annotate('', xy=(69, 56), xytext=(64.5, 56),
                arrowprops=dict(arrowstyle='<->', color='#38BDF8', lw=2.5, mutation_scale=16), zorder=6)
    
    # Badge for Token <-> Counter
    token_ctr_badge = patches.FancyBboxPatch(
        (64.8, 48), 4.4, 16,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor='#082F49', edgecolor='#38BDF8', linewidth=1.2, zorder=7
    )
    ax.add_patch(token_ctr_badge)
    ax.text(67, 56, "1 : N\n(Assigned)", color='#38BDF8', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=8)

    # 3. Token -> Service (References Service Catalog) - Left Horizontal Bridge
    ax.annotate('', xy=(31, 24), xytext=(36.5, 24),
                arrowprops=dict(arrowstyle='<-', color='#FBBF24', lw=2.5, mutation_scale=16), zorder=6)
    
    # Badge for Token -> Service
    token_svc_badge = patches.FancyBboxPatch(
        (31.8, 19), 4.4, 10,
        boxstyle="round,pad=0.2,rounding_size=0.8",
        facecolor='#451A03', edgecolor='#FBBF24', linewidth=1.2, zorder=7
    )
    ax.add_patch(token_svc_badge)
    ax.text(34, 24, "N : 1\n(Ref)", color='#FDE68A', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=8)

    # Legend / Key at Bottom Right (y=8 to 27)
    legend_box = patches.FancyBboxPatch(
        (69, 8), 27, 19,
        boxstyle="round,pad=0.4,rounding_size=1.2",
        facecolor='#0F172A', edgecolor='#334155', linewidth=1.5, zorder=4
    )
    ax.add_patch(legend_box)
    ax.text(82.5, 23.5, "Schema Relationship Key", color='#F8FAFC', fontsize=9.5, fontweight='bold', ha='center', zorder=5)
    
    ax.plot([71, 74], [19.5, 19.5], color='#A5B4FC', lw=2, ls=(0, (4, 3)))
    ax.text(75.5, 19.5, "Dotted: Staff Operator Auth Link", color='#C7D2FE', fontsize=8, va='center', zorder=5)
    
    ax.plot([71, 74], [15, 15], color='#38BDF8', lw=2)
    ax.text(75.5, 15, "Solid: Foreign Key (counterId)", color='#7DD3FC', fontsize=8, va='center', zorder=5)
    
    ax.plot([71, 74], [10.5, 10.5], color='#FBBF24', lw=2)
    ax.text(75.5, 10.5, "Orange: Service String Index Ref", color='#FDE68A', fontsize=8, va='center', zorder=5)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, '02_er_diagram.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0B132B')
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# 3. UI SCREENSHOTS / MOCKUPS (Slides 07 & 08)
# -----------------------------------------------------------------------------
def generate_ui_card(title, subtitle, badge_text, badge_col, bg_col, elements, out_name):
    fig, ax = plt.subplots(figsize=(6, 4.5), dpi=300)
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Phone / Device Window Container
    container = patches.FancyBboxPatch(
        (5, 5), 90, 90,
        boxstyle="round,pad=1,rounding_size=4",
        linewidth=2, edgecolor='#334155', facecolor='#111827', zorder=1
    )
    ax.add_patch(container)

    # Top Status Bar
    ax.plot([5, 95], [86, 86], color='#1F2937', lw=1.5)
    ax.text(10, 90, 'QFlow • Live', color='#6366F1', fontsize=10, fontweight='bold')
    ax.text(90, 90, 'WiFi Active', color='#10B981', fontsize=9, ha='right')

    # Header Title
    ax.text(50, 78, title, color='#F8FAFC', fontsize=14, fontweight='bold', ha='center')
    ax.text(50, 73, subtitle, color='#94A3B8', fontsize=9.5, ha='center')

    # Badge / Status
    if badge_text:
        badge = patches.FancyBboxPatch(
            (32, 63), 36, 6,
            boxstyle="round,pad=0.5,rounding_size=2",
            facecolor=badge_col, zorder=2
        )
        ax.add_patch(badge)
        ax.text(50, 66, badge_text, color='#FFFFFF', fontsize=10, fontweight='bold', ha='center', va='center', zorder=3)

    # Content Elements
    start_y = 54
    for elem in elements:
        if elem['type'] == 'box':
            b = patches.FancyBboxPatch(
                (12, elem['y']), 76, elem['h'],
                boxstyle="round,pad=0.5,rounding_size=2",
                linewidth=1, edgecolor=elem.get('border', '#374151'), facecolor=elem.get('bg', '#1F2937')
            )
            ax.add_patch(b)
            ax.text(16, elem['y'] + elem['h']/2, elem['label'], color='#94A3B8', fontsize=9, va='center')
            ax.text(84, elem['y'] + elem['h']/2, elem['val'], color=elem.get('val_col', '#F8FAFC'), fontsize=10, fontweight='bold', ha='right', va='center')
        elif elem['type'] == 'button':
            btn = patches.FancyBboxPatch(
                (12, elem['y']), 76, 9,
                boxstyle="round,pad=0.5,rounding_size=2.5",
                facecolor=elem.get('color', '#6366F1')
            )
            ax.add_patch(btn)
            ax.text(50, elem['y'] + 4.5, elem['text'], color='#FFFFFF', fontsize=11, fontweight='bold', ha='center', va='center')
        elif elem['type'] == 'big_number':
            ax.text(50, elem['y'], elem['number'], color=elem.get('color', '#818CF8'), fontsize=26, fontweight='black', ha='center')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, out_name)
    plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#0B0F19')
    plt.close()
    print(f"Generated: {out_path}")

# Generate 6 UI Mockup Screens
# Screen 1: Customer Form
generate_ui_card(
    "Customer Registration", "Scan QR Code -> Mobile Portal",
    "ENTER DETAILS", "#4F46E5", "#111827",
    [
        {'type': 'box', 'y': 44, 'h': 7, 'label': 'Full Name', 'val': 'Aditya PK'},
        {'type': 'box', 'y': 34, 'h': 7, 'label': 'Phone Number', 'val': '9876543210'},
        {'type': 'box', 'y': 24, 'h': 7, 'label': 'Service', 'val': 'Account Service'},
        {'type': 'button', 'y': 10, 'text': 'Get Instant Token ->', 'color': '#4F46E5'}
    ],
    '03_screen_customer_form.png'
)

# Screen 2: Token Status (WAITING)
generate_ui_card(
    "Your Live Token", "Real-Time Tracking & AI Wait",
    "STATUS: WAITING", "#D97706", "#111827",
    [
        {'type': 'big_number', 'y': 48, 'number': 'A101', 'color': '#818CF8'},
        {'type': 'box', 'y': 36, 'h': 8, 'label': 'Estimated Wait', 'val': '~8 Mins (AI)', 'val_col': '#F59E0B'},
        {'type': 'box', 'y': 26, 'h': 8, 'label': 'People Ahead', 'val': '1 in Queue', 'val_col': '#38BDF8'},
        {'type': 'box', 'y': 16, 'h': 8, 'label': 'Assigned', 'val': 'Counter 1 (Arun)', 'val_col': '#34D399'},
    ],
    '04_screen_token_status.png'
)

# Screen 3: Your Turn Alert
generate_ui_card(
    "YOUR TURN NOW!", "Audio Chime + Vibration + Screen Alert",
    "PROCEED TO COUNTER", "#059669", "#111827",
    [
        {'type': 'big_number', 'y': 48, 'number': 'A101', 'color': '#34D399'},
        {'type': 'box', 'y': 34, 'h': 10, 'label': 'Designated Counter', 'val': 'Counter 1', 'val_col': '#34D399', 'border': '#059669'},
        {'type': 'box', 'y': 21, 'h': 10, 'label': 'Staff Operator', 'val': 'Arun Kumar', 'val_col': '#F8FAFC'},
        {'type': 'button', 'y': 9, 'text': 'Service In Progress', 'color': '#059669'}
    ],
    '05_screen_your_turn.png'
)

# Screen 4: Staff Login
generate_ui_card(
    "Staff Portal Login", "Secure JWT Authentication",
    "STAFF / ADMIN", "#4F46E5", "#111827",
    [
        {'type': 'box', 'y': 46, 'h': 8, 'label': 'Email', 'val': 'admin@smartqueue.com'},
        {'type': 'box', 'y': 35, 'h': 8, 'label': 'Password', 'val': '••••••••'},
        {'type': 'box', 'y': 24, 'h': 8, 'label': 'Assigned Role', 'val': 'Admin / Staff', 'val_col': '#818CF8'},
        {'type': 'button', 'y': 10, 'text': 'Sign In to Dashboard', 'color': '#4F46E5'}
    ],
    '06_screen_staff_login.png'
)

# Screen 5: Staff Dashboard
generate_ui_card(
    "Staff Dashboard", "Active Counters & AI Engine",
    "LIVE OPERATIONS", "#0284C7", "#111827",
    [
        {'type': 'box', 'y': 46, 'h': 8, 'label': 'Counter 1 (Arun)', 'val': 'IN SERVICE (A101)', 'val_col': '#818CF8'},
        {'type': 'box', 'y': 35, 'h': 8, 'label': 'Counter 2 (Priya)', 'val': 'AVAILABLE', 'val_col': '#34D399'},
        {'type': 'box', 'y': 24, 'h': 8, 'label': 'AI Recommendation', 'val': 'Counter 2 (Optimal)', 'val_col': '#F59E0B'},
        {'type': 'button', 'y': 10, 'text': 'Call Next Customer', 'color': '#0284C7'}
    ],
    '07_screen_staff_dashboard.png'
)

# Screen 6: Queue & Counters Actions
generate_ui_card(
    "Queue & Token History", "Full Lifecycle Action Controls",
    "SYNCED WITH MONGODB", "#7C3AED", "#111827",
    [
        {'type': 'box', 'y': 46, 'h': 8, 'label': 'A101 - Aditya', 'val': 'Start / Complete', 'val_col': '#34D399'},
        {'type': 'box', 'y': 35, 'h': 8, 'label': 'A102 - Rahul', 'val': 'Waiting (Call)', 'val_col': '#F59E0B'},
        {'type': 'box', 'y': 24, 'h': 8, 'label': 'Action Suite', 'val': 'Skip / Transfer', 'val_col': '#C084FC'},
        {'type': 'button', 'y': 10, 'text': 'Refresh Live Queue', 'color': '#7C3AED'}
    ],
    '08_screen_queue_counters.png'
)

if __name__ == '__main__':
    generate_use_case_diagram()
    generate_er_diagram()
    print("All presentation diagrams and screenshots successfully generated!")
