import { useState, useEffect } from 'react';
import { QRCodeCanvas } from 'qrcode.react';
import { X, Download, Printer, ExternalLink, Wifi } from 'lucide-react';

const getCustomerURL = () => {
  const hostname = window.location.hostname;
  const port = window.location.port || '5173';
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    // Try to get LAN IP from the server
    return `http://${hostname}:${port}/customer`;
  }
  return `http://${hostname}:${port}/customer`;
};

const QRModal = ({ isOpen, onClose }) => {
  const [customerURL, setCustomerURL] = useState('');
  const [lanIP, setLanIP] = useState('');

  useEffect(() => {
    if (isOpen) {
      // Fetch LAN IP from backend
      const fetchLanIP = async () => {
        try {
          const hostname = window.location.hostname;
          const backendPort = '5000';
          const backendBase = hostname === 'localhost' || hostname === '127.0.0.1'
            ? `http://localhost:${backendPort}`
            : `http://${hostname}:${backendPort}`;
          
          const response = await fetch(`${backendBase}/api/health`);
          const data = await response.json();
          if (data.lanIP) {
            const url = `http://${data.lanIP}:5173/customer`;
            setCustomerURL(url);
            setLanIP(data.lanIP);
          } else {
            setCustomerURL(getCustomerURL());
          }
        } catch (e) {
          setCustomerURL(getCustomerURL());
        }
      };
      fetchLanIP();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleDownload = () => {
    const canvas = document.getElementById('qr-canvas');
    if (!canvas) return;
    const link = document.createElement('a');
    link.download = 'qflow-customer-qr.png';
    link.href = canvas.toDataURL();
    link.click();
  };

  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    const canvas = document.getElementById('qr-canvas');
    if (!canvas || !printWindow) return;
    
    const imgData = canvas.toDataURL();
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>QFlow Customer QR</title>
        <style>
          body { 
            font-family: Arial, sans-serif; 
            display: flex; 
            flex-direction: column;
            align-items: center; 
            padding: 40px;
            background: #ffffff;
          }
          h1 { font-size: 48px; margin-bottom: 8px; color: #1a1a2e; }
          h2 { font-size: 24px; color: #4b5563; margin-bottom: 4px; }
          .tagline { font-size: 18px; color: #6366f1; margin-bottom: 30px; }
          img { width: 350px; height: 350px; border: 3px solid #1a1a2e; padding: 10px; border-radius: 12px; }
          .scan-text { font-size: 22px; font-weight: bold; margin-top: 20px; color: #1a1a2e; }
          .steps { margin-top: 20px; text-align: left; font-size: 14px; color: #374151; }
          .steps li { margin: 6px 0; }
          .url { font-size: 12px; color: #6b7280; margin-top: 16px; font-family: monospace; }
          .wifi-note { margin-top: 10px; font-size: 12px; color: #9ca3af; font-style: italic; }
        </style>
      </head>
      <body>
        <h1>QFlow</h1>
        <h2>SMART QUEUE</h2>
        <div class="tagline">JOIN THE QUEUE</div>
        <img src="${imgData}" alt="QR Code" />
        <div class="scan-text">SCAN TO GET YOUR TOKEN</div>
        <ol class="steps">
          <li>Scan the QR code with your phone camera</li>
          <li>Enter your name and phone number</li>
          <li>Select your service type</li>
          <li>Receive your token instantly</li>
          <li>Track your queue status in real-time</li>
        </ol>
        <div class="url">${customerURL}</div>
        <div class="wifi-note">Connect to the Service Center Wi-Fi before scanning.</div>
      </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.print();
  };

  return (
    <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center px-4" onClick={onClose}>
      <div
        className="card w-full max-w-md animate-slide-up"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-xl font-bold text-white">Customer QR Code</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X size={20} />
          </button>
        </div>

        {/* QR Code */}
        {customerURL ? (
          <div className="flex flex-col items-center">
            <div className="bg-white p-4 rounded-2xl shadow-lg mb-4">
              <QRCodeCanvas
                id="qr-canvas"
                value={customerURL}
                size={220}
                bgColor="#ffffff"
                fgColor="#1a1a2e"
                level="H"
                includeMargin={false}
              />
            </div>

            {/* URL Display */}
            <div className="w-full mb-4 p-3 bg-gray-800 rounded-xl border border-gray-700">
              <p className="text-gray-400 text-xs mb-1 flex items-center gap-1">
                <Wifi size={11} /> Customer URL
              </p>
              <p className="text-indigo-400 font-mono text-sm break-all">{customerURL}</p>
              {lanIP && (
                <p className="text-gray-500 text-xs mt-1">LAN IP: {lanIP}</p>
              )}
            </div>

            {/* Info */}
            <div className="w-full mb-4 bg-amber-500/10 border border-amber-500/20 rounded-xl p-3">
              <p className="text-amber-400 text-xs">
                💡 Both the phone and laptop must be connected to the same Wi-Fi network.
                If the IP changes, run <code className="font-mono">npm run generate-qr</code> to regenerate.
              </p>
            </div>

            {/* Actions */}
            <div className="flex gap-3 w-full">
              <button
                onClick={handleDownload}
                className="btn-secondary flex-1 flex items-center justify-center gap-2"
              >
                <Download size={16} />
                Download
              </button>
              <button
                onClick={handlePrint}
                className="btn-secondary flex-1 flex items-center justify-center gap-2"
              >
                <Printer size={16} />
                Print
              </button>
              <a
                href={customerURL}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary flex items-center justify-center gap-2 px-4"
              >
                <ExternalLink size={16} />
              </a>
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
            <p className="text-gray-400">Generating QR...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default QRModal;
