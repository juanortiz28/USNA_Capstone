NRF.setAdvertising({}, { name: "JuanPuck", interval: 100 });
console.log("Puck.js MAC Address: " + NRF.getAddress());

let interval;
let txPower = -59;

// Function to calculate distance based on RSSI
function calculateDistance(rssi, txPower) {
  if (rssi === 0) {
    return -1; // Unable to determine distance
  }
  let ratio = rssi / txPower;
  if (ratio < 1.0) {
    return Math.pow(ratio, 10);
  } else {
    return 0.89976 * Math.pow(ratio, 7.7095) + 0.111;
  }
}

// Set up an RSSI handler
NRF.setRSSIHandler(function (rssi) {
  let distance = calculateDistance(rssi);
  console.log(`RSSI: ${rssi} dBm, Estimated Distance: ${distance.toFixed(2)} meters`);
});

// Start monitoring RSSI every 2 seconds
function startMonitoring() {
  console.log("Monitoring RSSI...");
  interval = setInterval(() => {
    // The handler will log RSSI automatically
  }, 2000);
}

// Stop monitoring RSSI
function stopMonitoring() {
  if (interval) {
    clearInterval(interval);
    console.log("Stopped monitoring RSSI.");
  }
}

// Start monitoring when the script is run
startMonitoring();


