const http = require('http');

http.get('http://localhost:5000/api/health', (res) => {
  if (res.statusCode === 200) {
    let raw = '';
    res.setEncoding('utf8');
    res.on('data', (chunk) => { raw += chunk; });
    res.on('end', () => {
      try {
        const data = JSON.parse(raw);
        console.log(`[ONLINE] QFlow backend is active on http://${data.lanIP}:5000`);
        process.exit(0);
      } catch (e) {
        process.exit(0);
      }
    });
  } else {
    process.exit(1);
  }
}).on('error', () => {
  console.log('[OFFLINE] QFlow backend server is not running yet.');
  process.exit(1);
});
