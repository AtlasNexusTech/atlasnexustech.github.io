const data = window.dashboardData || { lanes: [], deals: [], timeline: [] };
const laneList = document.querySelector('#laneList');
const dealList = document.querySelector('#dealList');
const timeline = document.querySelector('#timeline');
const sortBtn = document.querySelector('#sortBtn');

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, char => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  }[char]));
}

function statusRank(status) {
  return { blocked: 0, watch: 1, ship: 2 }[status] ?? 1;
}

function computeMetrics() {
  const lanes = data.lanes || [];
  const blockers = lanes.filter(item => item.status === 'blocked').length;
  const ready = lanes.filter(item => item.status === 'ship').length;
  const watch = lanes.filter(item => item.status === 'watch').length;
  const base = lanes.length ? Math.round(((ready * 100) + (watch * 62) + (blockers * 20)) / lanes.length) : 0;
  return {
    projects: lanes.length,
    opportunities: (data.deals || []).length,
    blockers,
    signal: Math.max(0, Math.min(100, base))
  };
}

function renderMetrics() {
  const metrics = computeMetrics();
  document.querySelector('#metric-projects').textContent = metrics.projects;
  document.querySelector('#metric-opportunities').textContent = metrics.opportunities;
  document.querySelector('#metric-blockers').textContent = metrics.blockers;
  document.querySelector('#metric-signal').textContent = `${metrics.signal}%`;

  const radial = document.querySelector('#radialScore');
  radial.style.setProperty('--score', metrics.signal);
  radial.querySelector('span').textContent = metrics.signal;

  const healthLabel = document.querySelector('#healthLabel');
  const healthCopy = document.querySelector('#healthCopy');
  if (metrics.blockers > 0) {
    healthLabel.textContent = 'Action requise';
    healthCopy.textContent = `${metrics.blockers} blocage à lever avant publication complète.`;
  } else if (metrics.signal >= 78) {
    healthLabel.textContent = 'Stable & publiable';
    healthCopy.textContent = 'Le cockpit est cohérent : les chantiers principaux peuvent être poussés et vérifiés.';
  } else {
    healthLabel.textContent = 'À prioriser';
    healthCopy.textContent = 'Quelques pistes restent à qualifier avant de parler de livraison.';
  }

  document.querySelector('#sideUpdated').textContent = `Mis à jour ${new Date().toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' })}`;
  document.querySelector('#focusTitle').textContent = data.focus?.title || 'Monétisation & livraison';
  document.querySelector('#focusCopy').textContent = data.focus?.copy || 'Prioriser ce qui peut être publié, vendu ou contacté maintenant.';
}

function renderLanes(items) {
  laneList.innerHTML = items.map(item => `
    <div class="lane">
      <div>
        <strong>${escapeHtml(item.title)}</strong>
        <p>${escapeHtml(item.detail)}</p>
        <div class="lane-meta">
          ${(item.tags || []).map(tag => `<span class="chip">${escapeHtml(tag)}</span>`).join('')}
        </div>
      </div>
      <span class="status ${escapeHtml(item.status)}">${escapeHtml(item.label)}</span>
    </div>
  `).join('');
}

function renderDeals() {
  dealList.innerHTML = (data.deals || []).map(deal => `
    <div class="deal">
      <div class="deal-top"><strong>${escapeHtml(deal.city)}</strong><em>${escapeHtml(deal.price)}</em></div>
      <p>${escapeHtml(deal.note)}</p>
      ${deal.risk ? `<small>${escapeHtml(deal.risk)}</small>` : ''}
    </div>
  `).join('');
}

function renderTimeline() {
  timeline.innerHTML = (data.timeline || []).map((step, index) => `
    <div class="step">
      <div class="num">${index + 1}</div>
      <strong>${escapeHtml(step.title)}</strong>
      <p>${escapeHtml(step.body)}</p>
      ${step.owner ? `<span class="owner">${escapeHtml(step.owner)}</span>` : ''}
    </div>
  `).join('');
}

function renderAll() {
  renderMetrics();
  renderLanes(data.lanes || []);
  renderDeals();
  renderTimeline();
}

renderAll();

sortBtn?.addEventListener('click', () => {
  const sorted = [...(data.lanes || [])].sort((a, b) => {
    if (statusRank(a.status) !== statusRank(b.status)) return statusRank(a.status) - statusRank(b.status);
    return (a.priority || 99) - (b.priority || 99);
  });
  renderLanes(sorted);
  sortBtn.textContent = 'Priorisé';
  window.setTimeout(() => { sortBtn.textContent = 'Prioriser'; }, 1400);
});
