# 🚀 QFlow: How to Run the Project & Network Setup Guide
**Department of AI & DS | Easwari Engineering College**  
**Student:** Adithya P K (310624243009) | **Project:** QFlow

---

## 1. Quick Summary of Your IP Address
- **Current Home Wi-Fi IP:** `192.168.1.7`
- **Customer Portal URL (Phone on Wi-Fi):** `http://192.168.1.7:5173/customer`
- **Staff Operations Dashboard (Laptop):** `http://localhost:5173/` (or `http://192.168.1.7:5173/`)
- **Backend API Server:** `http://localhost:5000`
- **Login Credentials:** `admin@smartqueue.com` / `admin123`

---

## 2. Option A: Testing Right Now on Your House Wi-Fi (Step-by-Step)

Follow these 4 simple steps to test it right now from your house:

### Step 1: Ensure Your Phone & Laptop are on the SAME House Wi-Fi
- Check your laptop Wi-Fi: Connected to your home router.
- Check your phone Wi-Fi: Connected to the **exact same home Wi-Fi name (SSID)**.
- **IMPORTANT:** On your phone, turn **OFF** Mobile Data (4G/5G) so the phone is forced to use the Wi-Fi network.

### Step 2: Start the Project
Double-click `START_QFLOW.bat` in the project root, or open Command Prompt / PowerShell in `c:\Projects\QFlow` and run:
```cmd
npm run dev
```
Wait 3–5 seconds until you see:
```
Backend:         http://localhost:5000
Frontend:        http://localhost:5173
Network:         http://192.168.1.7:5173
Customer Portal: http://192.168.1.7:5173/customer
MongoDB:         Connected
Socket.IO:       Ready
```

### Step 3: Open Staff Dashboard on Laptop
- Your browser will open to `http://localhost:5173/` automatically.
- Login with:
  - **Email:** `admin@smartqueue.com`
  - **Password:** `admin123`
- You will see the active counters (Counters 1, 2, 3, 4) and live queue.

### Step 4: Open Customer Portal on Your Phone
On your phone browser (Safari / Chrome), you have two choices:
1. **Choice 1 (Scan QR):** On the laptop dashboard, click the **"Customer QR"** button in the left sidebar $\rightarrow$ point your phone camera at the screen $\rightarrow$ tap the link.
2. **Choice 2 (Type URL):** Open Safari/Chrome on phone and type:
   ```
   http://192.168.1.7:5173/customer
   ```
- You will see the dark-themed mobile page: **"Join the Queue"**.
- Enter your name `"Adithya"`, phone number, select `"Account Service"`, and tap **"Get Token"**.
- Token **A101** will appear on your phone, and simultaneously appear on your laptop!

---

## 3. Option B: Switching to Mobile Hotspot Tomorrow at the College Lab (Step-by-Step)

When you arrive at the college lab tomorrow, if college Wi-Fi has isolation or doesn't work, **use Mobile Hotspot**:

### Step 1: Turn ON Hotspot on Your Phone
1. Go to your phone Settings $\rightarrow$ **Personal Hotspot** $\rightarrow$ Turn **ON**.
2. Make sure you know your hotspot Wi-Fi password.

### Step 2: Connect Laptop to Your Phone Hotspot
1. On your laptop, click the Wi-Fi icon on the Windows taskbar.
2. Select your phone's hotspot name $\rightarrow$ enter password $\rightarrow$ Connect.
3. *Now your laptop and phone are the only two devices on a direct private network.*

### Step 3: Refresh the Network IP & QR Code
In `c:\Projects\QFlow`, double click `CHECK_NETWORK_IP.bat` (or run in terminal):
```cmd
npm run generate-qr
```
The terminal will display your new hotspot IP (typically `192.168.43.XX`).

### Step 4: Start QFlow
Double-click `START_QFLOW.bat` (or run `npm run dev`).
The terminal will print:
```
Network:         http://192.168.43.XX:5173
Customer Portal: http://192.168.43.XX:5173/customer
```
Now scan the QR or open `http://192.168.43.XX:5173/customer` on your phone!

---

## 4. Option C: Zero-Network Projector Fallback (100% Fail-Safe)
If for any reason you do not want to use Wi-Fi or Hotspot in front of the examiners:
1. Open Google Chrome on your laptop.
2. **Left Half of Screen:** Open `http://localhost:5173/` (Staff Dashboard).
3. **Right Half of Screen:** Open another Chrome Incognito window to `http://localhost:5173/customer`.
4. Press `F12` $\rightarrow$ click the **Device Toolbar (Ctrl+Shift+M)** $\rightarrow$ select **iPhone 14 Pro**.
5. Both screens run side-by-side on your laptop screen! Everything syncs live over WebSockets without touching any Wi-Fi router.

---

## 5. Troubleshooting Cheat Sheet

| Issue | Cause | 1-Second Solution |
| :--- | :--- | :--- |
| **Phone says "Site can't be reached"** | Phone is on mobile 5G data instead of Wi-Fi | Turn OFF mobile data on phone; ensure Wi-Fi SSID matches laptop. |
| **IP changed after connecting to new Wi-Fi** | DHCP assigned new IP address | Run `CHECK_NETWORK_IP.bat` or restart `npm run dev` to pick up new IP. |
| **Windows Firewall prompt appeared** | Windows blocked port 5173/5000 | Click **"Allow Access"** on Private and Public networks. |
| **Port 5000 or 5173 already in use** | A previous Node process is still running in background | Open Command Prompt and run: `taskkill /F /IM node.exe` then run `npm run dev`. |
| **Need to reset tokens to clean demo state** | Old test tokens accumulated | Double-click `RESEED_DATABASE.bat` or run `npm run seed`. |
