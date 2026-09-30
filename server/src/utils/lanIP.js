const os = require('os');

/**
 * Detects the machine's LAN IP address (192.168.x.x, 10.x.x.x, or 172.16-31.x.x).
 * Falls back to 127.0.0.1 if none found.
 */
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
          // Exclude typical VirtualBox default network (192.168.56.x) from priority candidates
          const isVboxDefault = ip.startsWith('192.168.56.');
          candidates.push({
            ip,
            priority: (isVirtual || isVboxDefault) ? 1 : 10,
          });
        }
      }
    }
  }

  // Pick highest priority IP (physical Wi-Fi/LAN first)
  if (candidates.length > 0) {
    candidates.sort((a, b) => b.priority - a.priority);
    return candidates[0].ip;
  }

  return '127.0.0.1';
}

module.exports = { getLanIP };
