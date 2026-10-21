import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_system_architecture():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    font_family = 'DejaVu Sans'

    # 1. User Roles (Top Row)
    roles = [
        ("Customer\n(Mobile Web)", 12.5),
        ("Counter Teller\n(Workstation)", 37.5),
        ("Queue Supervisor\n(Operations)", 62.5),
        ("Administrator\n(System Config)", 87.5)
    ]
    for title, cx in roles:
        box = patches.FancyBboxPatch((cx - 10, 89), 20, 8, boxstyle="round,pad=0.3,rounding_size=1.5",
                                     facecolor="#FFFFFF", edgecolor="#000000", linewidth=1.5)
        ax.add_patch(box)
        ax.text(cx, 93, title, ha='center', va='center', fontsize=9, fontweight='bold', color="#000000", fontfamily=font_family)

    # Down arrows from users to presentation layer
    for _, cx in roles:
        ax.annotate('', xy=(cx, 84), xytext=(cx, 89),
                    arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))

    # 2. Presentation Layer
    pres_box = patches.Rectangle((4, 64), 92, 20, facecolor="#FAFAFA", edgecolor="#000000", linewidth=1.5)
    ax.add_patch(pres_box)
    ax.text(6, 81.5, "PRESENTATION LAYER  (Client Container / Web Browser, Port 3000)", fontsize=10, fontweight='bold', color="#000000", fontfamily=font_family)

    # Presentation inner box
    pres_inner = patches.FancyBboxPatch((7, 66), 86, 13.5, boxstyle="round,pad=0.2,rounding_size=1",
                                        facecolor="#FFFFFF", edgecolor="#000000", linewidth=1.0)
    ax.add_patch(pres_inner)
    ax.text(50, 76, "Mobile Web Browser & Desktop Workstations (Safari • Chrome • Edge)", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(50, 72, "React 19 SPA • Tailwind CSS • Lucide Icons • Socket.IO Client • Recharts Telemetry", ha='center', va='center', fontsize=8.5, color="#1F2937", fontfamily=font_family)
    ax.text(50, 68, "Modules: Dynamic QR Portal • Personal Token Tracker • Teller Workstation • Supervisor Analytics • Vibration / Push Alerts", ha='center', va='center', fontsize=8, fontstyle='italic', color="#374151", fontfamily=font_family)

    # Arrow from Presentation to Application
    ax.annotate('', xy=(50, 58), xytext=(50, 64),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.5))
    ax.text(50, 60.5, "JSON over HTTP (REST API, Bearer JWT)   |   Full-Duplex WebSockets (Socket.IO)",
            ha='center', va='center', fontsize=8, fontweight='bold', color="#000000",
            bbox=dict(boxstyle="square,pad=0.2", facecolor="#F3F4F6", edgecolor="#000000", lw=0.8))

    # 3. Application Layer
    app_box = patches.Rectangle((4, 21), 92, 37, facecolor="#F9FAFB", edgecolor="#000000", linewidth=1.5)
    ax.add_patch(app_box)
    ax.text(6, 55.5, "APPLICATION LAYER  (Server Container / Node.js Runtime, Port 5000)", fontsize=10, fontweight='bold', color="#000000", fontfamily=font_family)

    # Middleware box
    mw_box = patches.FancyBboxPatch((7, 47.5), 86, 6.5, boxstyle="round,pad=0.2,rounding_size=1",
                                    facecolor="#FFFFFF", edgecolor="#000000", linewidth=1)
    ax.add_patch(mw_box)
    ax.text(50, 52, "Middleware Pipeline", ha='center', va='center', fontsize=9, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(50, 49.2, "Helmet Security • CORS Whitelisting • JSON Body Parser • JWT Bearer Auth Guard • Error Handler", ha='center', va='center', fontsize=8, color="#1F2937", fontfamily=font_family)

    # Arrow mw to routes
    ax.annotate('', xy=(50, 44), xytext=(50, 47.5),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1))

    # Routes & Controllers
    routes_box = patches.FancyBboxPatch((7, 34.5), 86, 9.5, boxstyle="round,pad=0.2,rounding_size=1",
                                        facecolor="#FFFFFF", edgecolor="#000000", linewidth=1)
    ax.add_patch(routes_box)
    ax.text(50, 41.5, "Routes & Controllers", ha='center', va='center', fontsize=9, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(50, 38.5, "/api/tokens  •  /api/counters  •  /api/services  •  /api/auth  •  /api/analytics  •  /api/health", ha='center', va='center', fontsize=8.5, color="#000000", fontfamily='Courier New', fontweight='bold')
    ax.text(50, 36, "Token Controller • Counter Controller • Service Controller • Auth Controller • Analytics Controller", ha='center', va='center', fontsize=8, color="#374151", fontfamily=font_family)

    # Sub-engines in Application Layer
    ai_box = patches.FancyBboxPatch((7, 23), 41, 9.5, boxstyle="round,pad=0.2,rounding_size=1",
                                    facecolor="#FFFFFF", edgecolor="#000000", linewidth=1)
    ax.add_patch(ai_box)
    ax.text(27.5, 30, "AI Prediction & Heuristic Recommender", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(27.5, 27, "Synthetic baseline regression + Peak hour scale", ha='center', va='center', fontsize=7.5, color="#1F2937", fontfamily=font_family)
    ax.text(27.5, 24.5, "100-pt dynamic counter workload scoring", ha='center', va='center', fontsize=7.5, color="#1F2937", fontfamily=font_family)

    sock_box = patches.FancyBboxPatch((52, 23), 41, 9.5, boxstyle="round,pad=0.2,rounding_size=1",
                                      facecolor="#FFFFFF", edgecolor="#000000", linewidth=1)
    ax.add_patch(sock_box)
    ax.text(72.5, 30, "Socket.IO Real-Time Multiplexing", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(72.5, 27, "Rooms: 'queue' (global) • 'token:{id}' (mobile)", ha='center', va='center', fontsize=7.5, color="#1F2937", fontfamily=font_family)
    ax.text(72.5, 24.5, "Events: token:created • token:called • queue:update", ha='center', va='center', fontsize=7.5, color="#1F2937", fontfamily=font_family)

    # Arrow from App Layer to Data Layer
    ax.annotate('', xy=(27.5, 16), xytext=(27.5, 21),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.5))
    ax.annotate('', xy=(72.5, 16), xytext=(72.5, 21),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.5))

    # 4. Data Layer
    data_box = patches.Rectangle((4, 2), 92, 14, facecolor="#FAFAFA", edgecolor="#000000", linewidth=1.5)
    ax.add_patch(data_box)
    ax.text(6, 13.5, "DATA LAYER  (MongoDB 7.0 Document Database, Port 27017)", fontsize=10, fontweight='bold', color="#000000", fontfamily=font_family)

    col_box = patches.FancyBboxPatch((7, 3.5), 58, 8.5, boxstyle="round,pad=0.2,rounding_size=1",
                                     facecolor="#FFFFFF", edgecolor="#000000", linewidth=1)
    ax.add_patch(col_box)
    ax.text(36, 9.5, "MongoDB Persistent Collections (Mongoose Schemas)", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(36, 6.5, "tokens  •  counters  •  services  •  users  •  synthetic_durations", ha='center', va='center', fontsize=8, color="#000000", fontfamily='Courier New', fontweight='bold')

    seed_box = patches.FancyBboxPatch((68, 3.5), 25, 8.5, boxstyle="round,pad=0.2,rounding_size=1",
                                      facecolor="#FFFFFF", edgecolor="#000000", linewidth=1)
    ax.add_patch(seed_box)
    ax.text(80.5, 9.5, "Synthetic Data / Cache", ha='center', va='center', fontsize=8.5, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(80.5, 6.5, "historicalDurations.json\nMemory Fallback Engine", ha='center', va='center', fontsize=7.5, color="#1F2937", fontfamily=font_family)

    plt.tight_layout()
    out_path = r'c:\Projects\QFlow\presentation_images\fig_4_1_architecture.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated B&W {out_path}")

def create_deployment_architecture():
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    font_family = 'DejaVu Sans'

    # 1. Top Client Devices
    top_box = patches.FancyBboxPatch((15, 84), 70, 12, boxstyle="round,pad=0.3,rounding_size=1.5",
                                     facecolor="#FFFFFF", edgecolor="#000000", linewidth=1.5)
    ax.add_patch(top_box)
    ax.text(50, 92.5, "Client Devices on Local Wi-Fi Network / Internet", ha='center', va='center', fontsize=10, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(50, 89, "Customer Smartphone (Safari / Chrome): http://192.168.1.x:3000/register", ha='center', va='center', fontsize=8.5, color="#000000", fontfamily='Courier New')
    ax.text(50, 86, "Staff / Admin Workstation (Edge / Chrome): http://localhost:3000/dashboard", ha='center', va='center', fontsize=8.5, color="#000000", fontfamily='Courier New')

    # Big Host Machine Container
    host_box = patches.Rectangle((6, 4), 88, 74, facecolor="#FAFAFA", edgecolor="#000000", linewidth=1.8, linestyle='--')
    ax.add_patch(host_box)
    ax.text(9, 75, "Host Server / Docker Compose Network (qflow-net)", fontsize=10.5, fontweight='bold', color="#000000", fontfamily=font_family)

    # Arrows from client to containers
    ax.annotate('', xy=(32, 67), xytext=(32, 84),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.5))
    ax.text(32, 77, "HTTP / HTTPS (Port 3000)", ha='center', va='center', fontsize=8, color="#000000",
            bbox=dict(boxstyle="square,pad=0.2", facecolor="#F3F4F6", edgecolor="#000000", lw=0.6))

    ax.annotate('', xy=(68, 67), xytext=(68, 84),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.5))
    ax.text(68, 77, "WebSocket / REST (Port 5000)", ha='center', va='center', fontsize=8, color="#000000",
            bbox=dict(boxstyle="square,pad=0.2", facecolor="#F3F4F6", edgecolor="#000000", lw=0.6))

    # 2. Client Container Box
    client_box = patches.FancyBboxPatch((12, 45), 38, 22, boxstyle="round,pad=0.3,rounding_size=1.2",
                                        facecolor="#FFFFFF", edgecolor="#000000", linewidth=1.5)
    ax.add_patch(client_box)
    ax.text(31, 63.5, "client (Frontend Service)", ha='center', va='center', fontsize=10, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(31, 59.5, "Base Image: node:22-alpine / Nginx", ha='center', va='center', fontsize=8, fontstyle='italic', color="#374151", fontfamily=font_family)
    ax.text(31, 56, "Container Port: 3000 (Host: 3000)", ha='center', va='center', fontsize=8, color="#000000", fontfamily=font_family)
    ax.text(31, 52.5, "React 19 SPA + Vite Production Build", ha='center', va='center', fontsize=8, fontweight='bold', color="#1F2937", fontfamily=font_family)
    ax.text(31, 48.5, "Tailwind CSS • Lucide • Socket.IO Client", ha='center', va='center', fontsize=7.5, color="#374151", fontfamily=font_family)

    # 3. Server Container Box
    server_box = patches.FancyBboxPatch((52, 45), 38, 22, boxstyle="round,pad=0.3,rounding_size=1.2",
                                        facecolor="#FFFFFF", edgecolor="#000000", linewidth=1.5)
    ax.add_patch(server_box)
    ax.text(71, 63.5, "server (Backend API Service)", ha='center', va='center', fontsize=10, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(71, 59.5, "Base Image: node:22-alpine", ha='center', va='center', fontsize=8, fontstyle='italic', color="#374151", fontfamily=font_family)
    ax.text(71, 56, "Container Port: 5000 (Host: 5000)", ha='center', va='center', fontsize=8, color="#000000", fontfamily=font_family)
    ax.text(71, 52.5, "Express.js REST Engine + Socket.IO Server", ha='center', va='center', fontsize=8, fontweight='bold', color="#1F2937", fontfamily=font_family)
    ax.text(71, 48.5, "Prediction Engine • Dynamic Recommender", ha='center', va='center', fontsize=7.5, color="#374151", fontfamily=font_family)

    # Horizontal communication between Client and Server
    ax.annotate('', xy=(52, 54), xytext=(50, 54),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))
    ax.text(51, 57, "HTTP / WS", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#000000",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="#F3F4F6", edgecolor="#000000", lw=0.5))

    # Arrow down from server to database
    ax.annotate('', xy=(51, 31), xytext=(71, 45),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.5))
    ax.text(64, 38, "Mongoose Driver (Port 27017)", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#000000",
            bbox=dict(boxstyle="square,pad=0.2", facecolor="#F3F4F6", edgecolor="#000000", lw=0.6))

    # 4. Database Services (Bottom Row)
    db_box1 = patches.FancyBboxPatch((15, 10), 32, 19, boxstyle="round,pad=0.3,rounding_size=1.2",
                                     facecolor="#FFFFFF", edgecolor="#000000", linewidth=1.5)
    ax.add_patch(db_box1)
    ax.text(31, 25, "mongodb (Database Service)", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(31, 21.5, "Image: mongo:7.0 / mongo:7.0-jammy", ha='center', va='center', fontsize=8, fontstyle='italic', color="#374151", fontfamily=font_family)
    ax.text(31, 18, "Port: 27017 (Internal Bridge)", ha='center', va='center', fontsize=8, color="#000000", fontfamily=font_family)
    ax.text(31, 14.5, "Volume: /data/db (Persistent Storage)", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#1F2937", fontfamily=font_family)

    db_box2 = patches.FancyBboxPatch((53, 10), 32, 19, boxstyle="round,pad=0.3,rounding_size=1.2",
                                     facecolor="#FFFFFF", edgecolor="#000000", linewidth=1.5, linestyle=':')
    ax.add_patch(db_box2)
    ax.text(69, 25, "In-Memory DB (Dev Fallback)", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#000000", fontfamily=font_family)
    ax.text(69, 21.5, "Library: MongoMemoryServer v9.1", ha='center', va='center', fontsize=8, fontstyle='italic', color="#374151", fontfamily=font_family)
    ax.text(69, 18, "Zero-Config Standalone Execution", ha='center', va='center', fontsize=8, color="#000000", fontfamily=font_family)
    ax.text(69, 14.5, "Automated Mock Seeding & Teardown", ha='center', va='center', fontsize=7.5, color="#1F2937", fontfamily=font_family)

    ax.annotate('', xy=(31, 29), xytext=(55, 45),
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))

    plt.tight_layout()
    out_path = r'c:\Projects\QFlow\presentation_images\fig_4_2_deployment.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated B&W {out_path}")

if __name__ == '__main__':
    create_system_architecture()
    create_deployment_architecture()
