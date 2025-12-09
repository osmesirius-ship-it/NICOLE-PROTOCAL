function statusChip(status) {
  const map = {
    healthy: { label: 'Operational', className: 'status-ok' },
    warning: { label: 'Degraded', className: 'status-warn' },
    risky: { label: 'Risky', className: 'status-risk' }
  };
  const meta = map[status] ?? map.healthy;
  return `<span class="status"><span class="status-dot ${meta.className}"></span>${meta.label}</span>`;
}

export function renderModules(container, modules) {
  container.innerHTML = modules
    .map(
      (mod) => `
      <article class="module-card">
        <div class="title">
          <h3>${mod.name}</h3>
          <span class="layer-chip">${mod.layer}</span>
        </div>
        <p>${mod.description}</p>
        <div class="stack">${mod.interfaces.map((i) => `<span>${i}</span>`).join('')}</div>
        <div>${statusChip(mod.status)}</div>
      </article>
    `
    )
    .join('');
}
