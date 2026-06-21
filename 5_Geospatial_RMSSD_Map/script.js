let map, markers = [], allData = [], currentThreshold = 50;

map = L.map('map').setView([40.2033, -8.4103], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function norm(k) { return k.trim().toLowerCase().replace(/[\s_\-]/g, ''); }

function findCol(row, candidates) {
  for (const k of Object.keys(row)) {
    if (candidates.includes(norm(k))) return k;
  }
  return null;
}

function renderMarkers(threshold) {
  markers.forEach(m => map.removeLayer(m));
  markers = [];
  let low = 0, high = 0;
  allData.forEach(row => {
    const lat = parseFloat(row._lat);
    const lng = parseFloat(row._lng);
    const val = parseFloat(row._rmssd);
    if (isNaN(lat) || isNaN(lng) || isNaN(val)) return;
    const isHigh = val >= threshold;
    isHigh ? high++ : low++;
    const color = isHigh ? '#27ae60' : '#e74c3c';
    const border = isHigh ? '#1e8449' : '#c0392b';
    const m = L.circleMarker([lat, lng], {
      radius: 9,
      fillColor: color,
      color: border,
      weight: 2,
      opacity: 1,
      fillOpacity: 0.85
    });
    const extra = Object.keys(row).filter(k => !['_lat','_lng','_rmssd'].includes(k));
    const extraHtml = extra.map(k => `<tr><td style="color:#999;padding:2px 10px 2px 0;font-size:12px">${k}</td><td style="font-size:12px"><b>${row[k]}</b></td></tr>`).join('');
    m.bindPopup(`
      <div style="font-size:13px;min-width:160px;font-family:system-ui">
        <div style="font-weight:600;margin-bottom:8px;font-size:14px;color:${color}">
          RMSSD: ${val.toFixed(3)}
        </div>
        <table style="border-collapse:collapse;width:100%">
          <tr><td style="color:#999;padding:2px 10px 2px 0;font-size:12px">Latitude</td><td style="font-size:12px">${lat.toFixed(6)}</td></tr>
          <tr><td style="color:#999;padding:2px 10px 2px 0;font-size:12px">Longitude</td><td style="font-size:12px">${lng.toFixed(6)}</td></tr>
          ${extraHtml}
        </table>
      </div>
    `);
    m.addTo(map);
    markers.push(m);
  });
  document.getElementById('count-total').textContent = allData.length;
  document.getElementById('count-high').textContent = high;
  document.getElementById('count-low').textContent = low;
  document.getElementById('threshold-display-val').textContent = threshold.toFixed(3);
}

document.getElementById('file-input').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const wb = XLSX.read(new Uint8Array(ev.target.result), { type: 'array' });
      const rows = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
      if (!rows.length) return;

      const s = rows[0];
      const latKey   = findCol(s, ['latitude','lat']);
      const lngKey   = findCol(s, ['longitude','lon','lng','long']);
      const rmssdKey = findCol(s, ['rmssd']);

      if (!latKey || !lngKey || !rmssdKey) return;

      allData = rows.map(r => {
        const c = Object.assign({}, r);
        c._lat = r[latKey];
        c._lng = r[lngKey];
        c._rmssd = r[rmssdKey];
        return c;
      }).filter(r => !isNaN(parseFloat(r._rmssd)));

      const vals = allData.map(r => parseFloat(r._rmssd)).sort((a, b) => a - b);
      const minV = vals[0], maxV = vals[vals.length - 1];
      currentThreshold = vals[Math.floor(vals.length / 2)];

      const sl = document.getElementById('threshold-slider');
      sl.min = minV;
      sl.max = maxV;
      sl.step = ((maxV - minV) / 200).toFixed(6);
      sl.value = currentThreshold;
      sl.disabled = false;
      updateSliderGradient(sl);

      const lats = allData.map(r => parseFloat(r._lat));
      const lngs = allData.map(r => parseFloat(r._lng));
      map.fitBounds([
        [Math.min(...lats), Math.min(...lngs)],
        [Math.max(...lats), Math.max(...lngs)]
      ], { padding: [40, 40] });

      renderMarkers(currentThreshold);
    } catch (err) {
      console.error(err);
    }
  };
  reader.readAsArrayBuffer(file);
});

function updateSliderGradient(slider) {
  const min = parseFloat(slider.min) || 0;
  const max = parseFloat(slider.max) || 100;
  const val = parseFloat(slider.value);
  const pct = ((val - min) / (max - min)) * 100;
  slider.style.background = `linear-gradient(to right, #e74c3c 0%, #e74c3c ${pct}%, #27ae60 ${pct}%, #27ae60 100%)`;
  const label = document.getElementById('thumb-label');
  label.textContent = val.toFixed(3);
  label.style.left = `calc(${pct}% + ${9 - pct * 0.18}px)`;
}

document.getElementById('threshold-slider').addEventListener('input', e => {
  currentThreshold = parseFloat(e.target.value);
  updateSliderGradient(e.target);
  renderMarkers(currentThreshold);
});