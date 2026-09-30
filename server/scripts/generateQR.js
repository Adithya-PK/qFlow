/**
 * QFlow QR Code Generator
 *
 * Generates QR codes for the customer-facing token booking page.
 * Detects the machine's LAN IP automatically.
 *
 * Output files (in qr/ at project root):
 *   - customer-qr.png       (400px — quick sharing)
 *   - customer-qr.svg       (vector — scalable)
 *   - customer-qr-print.png (1200px — high-res for printing)
 *
 * Usage: npm run generate-qr
 */

const QRCode = require('qrcode');
const os = require('os');
const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// LAN IP detection (same logic as lanIP.js — standalone for this script)
// ---------------------------------------------------------------------------
function getLanIP() {
  const interfaces = os.networkInterfaces();
  const candidates = [];

  for (const name of Object.keys(interfaces)) {
    const isVirtual = /virtual|vbox|vmware|wsl|hyper-v|loopback|pseudo/i.test(name);
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        const ip = iface.address;
        const isPrivate =
          ip.startsWith('192.168.') ||
          ip.startsWith('10.') ||
          (ip.startsWith('172.') &&
            parseInt(ip.split('.')[1], 10) >= 16 &&
            parseInt(ip.split('.')[1], 10) <= 31);

        if (isPrivate) {
          const isVboxDefault = ip.startsWith('192.168.56.');
          candidates.push({
            ip,
            priority: (isVirtual || isVboxDefault) ? 1 : 10,
          });
        }
      }
    }
  }

  if (candidates.length > 0) {
    candidates.sort((a, b) => b.priority - a.priority);
    return candidates[0].ip;
  }

  return '127.0.0.1';
}

// ---------------------------------------------------------------------------
// Main generator
// ---------------------------------------------------------------------------
async function generateQR() {
  const lanIP = getLanIP();
  const PORT = process.env.VITE_PORT || 5173;
  const customerURL = `http://${lanIP}:${PORT}/customer`;

  console.log('\n========================================');
  console.log('  QFlow QR Code Generator');
  console.log('========================================');
  console.log(`  LAN IP:       ${lanIP}`);
  console.log(`  Customer URL: ${customerURL}`);
  console.log('');

  // Ensure output directory exists at <project root>/qr/
  const qrDir = path.join(__dirname, '..', '..', 'qr');
  fs.mkdirSync(qrDir, { recursive: true });
  console.log(`  Output dir:   ${qrDir}`);
  console.log('');

  const qrOptions = {
    color: {
      dark: '#1a1a2e',   // Dark navy for QR modules
      light: '#ffffff',   // White background
    },
  };

  // 1. Standard PNG (400px)
  const pngPath = path.join(qrDir, 'customer-qr.png');
  await QRCode.toFile(pngPath, customerURL, { ...qrOptions, width: 400, margin: 2 });
  console.log(`  ✓ customer-qr.png       (400px)`);

  // 2. SVG (vector, no fixed size)
  const svgPath = path.join(qrDir, 'customer-qr.svg');
  const svgString = await QRCode.toString(customerURL, { type: 'svg', width: 400, margin: 2, ...qrOptions });
  fs.writeFileSync(svgPath, svgString, 'utf8');
  console.log(`  ✓ customer-qr.svg       (vector)`);

  // 3. High-res printable PNG (1200px)
  const printPath = path.join(qrDir, 'customer-qr-print.png');
  await QRCode.toFile(printPath, customerURL, { ...qrOptions, width: 1200, margin: 4 });
  console.log(`  ✓ customer-qr-print.png (1200px)`);

  // 4. Standalone Printable A4 Poster (HTML format - open in browser & Ctrl+P)
  const qrDataUri = await QRCode.toDataURL(customerURL, { ...qrOptions, width: 600, margin: 2 });
  const posterHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>QFlow - Smart Queue Poster</title>
  <style>
    @page { size: A4 portrait; margin: 0; }
    body {
      margin: 0;
      padding: 40px;
      box-sizing: border-box;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: #ffffff;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      min-height: 100vh;
      text-align: center;
    }
    .header { margin-top: 10px; }
    .brand { font-size: 54px; font-weight: 900; letter-spacing: 4px; color: #4f46e5; margin: 0; }
    .subtitle { font-size: 26px; font-weight: 700; color: #64748b; letter-spacing: 2px; margin: 8px 0 0; }
    .hero-box {
      background: #f8fafc;
      border: 3px solid #e2e8f0;
      border-radius: 24px;
      padding: 30px;
      margin: 25px 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .join-title { font-size: 32px; font-weight: 800; color: #0f172a; margin: 0 0 16px; }
    .qr-frame {
      background: #ffffff;
      padding: 16px;
      border: 4px solid #4f46e5;
      border-radius: 20px;
      box-shadow: 0 8px 24px rgba(79, 70, 229, 0.15);
    }
    .qr-frame img { width: 340px; height: 340px; display: block; }
    .scan-prompt { font-size: 24px; font-weight: 800; color: #4f46e5; margin: 18px 0 0; }
    .steps-container {
      width: 100%;
      max-width: 500px;
      background: #ffffff;
      border-radius: 16px;
      padding: 18px 24px;
      text-align: left;
      margin-top: 20px;
      border: 1px solid #e2e8f0;
    }
    .step { font-size: 17px; font-weight: 600; color: #334155; margin: 8px 0; display: flex; align-items: center; }
    .step-num {
      background: #4f46e5;
      color: #ffffff;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: 800;
      margin-right: 12px;
      flex-shrink: 0;
    }
    .footer {
      margin-bottom: 10px;
      border-top: 2px dashed #cbd5e1;
      padding-top: 16px;
      width: 100%;
      max-width: 550px;
    }
    .wifi-notice { font-size: 15px; font-weight: 700; color: #b45309; background: #fef3c7; padding: 10px 16px; border-radius: 8px; display: inline-block; margin-bottom: 8px; }
    .url-text { font-family: monospace; font-size: 14px; color: #64748b; margin: 4px 0 0; }
    @media print {
      body { padding: 30px; }
      .hero-box { box-shadow: none; }
    }
  </style>
</head>
<body>
  <div class="header">
    <h1 class="brand">QFLOW</h1>
    <div class="subtitle">SMART QUEUE</div>
  </div>

  <div class="hero-box">
    <div class="join-title">JOIN THE QUEUE</div>
    <div class="qr-frame">
      <img src="${qrDataUri}" alt="QFlow Customer QR Code">
    </div>
    <div class="scan-prompt">Scan to Get Your Token</div>

    <div class="steps-container">
      <div class="step"><span class="step-num">1</span> Scan the QR</div>
      <div class="step"><span class="step-num">2</span> Enter Your Details</div>
      <div class="step"><span class="step-num">3</span> Select Your Service</div>
      <div class="step"><span class="step-num">4</span> Receive Your Token</div>
      <div class="step"><span class="step-num">5</span> Track Your Queue Status</div>
    </div>
  </div>

  <div class="footer">
    <div class="wifi-notice">Connect to the Service Center Wi-Fi before scanning.</div>
    <div class="url-text">${customerURL}</div>
  </div>
</body>
</html>`;

  fs.writeFileSync(path.join(qrDir, 'customer-poster.html'), posterHtml, 'utf8');
  console.log(`  ✓ customer-poster.html  (A4 Printable Poster)`);

  console.log('');
  console.log('  QR Files saved to: qr/');
  console.log('  Scan to open:      ' + customerURL);
  console.log('========================================\n');
}

generateQR().catch((err) => {
  console.error('\n[QR Generator] Error:', err.message);
  process.exit(1);
});
