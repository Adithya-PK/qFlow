const os = require('os');

/**
 * Detects the machine's active LAN IP address (192.168.x.x, 10.x.x.x, or 172.16-31.x.x).
 * Prioritizes Wi-Fi / Hotspot interfaces, then physical Ethernet, and deprioritizes virtual adapters.
 * Falls back to 127.0.0.1 if none found.
 */
function getLanIP() {
  const interfaces = os.networkInterfaces();
  const candidates = [];

  for (const name of Object.keys(interfaces)) {
    const isVirtual = /virtual|vbox|vmware|wsl|hyper-v|loopback|pseudo|docker|tailscale|zerotier/i.test(name);
    const isWiFi = /wi-fi|wlan|wireless|airport|hotspot/i.test(name);

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
          let priority = 10;

          if (isVirtual || isVboxDefault) {
            priority = 1;
          } else if (isWiFi) {
            // Wi-Fi / Hotspot has the absolute highest priority for mobile QR scanning
            priority = 20;
          }

          candidates.push({
            name,
            ip,
            priority,
          });
        }
      }
    }
  }

  // Pick highest priority IP (Wi-Fi/Hotspot first, then physical LAN, virtual last)
  if (candidates.length > 0) {
    candidates.sort((a, b) => b.priority - a.priority);
    return candidates[0].ip;
  }

  return '127.0.0.1';
}

module.exports = { getLanIP };
