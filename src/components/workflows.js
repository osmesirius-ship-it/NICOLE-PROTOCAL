import { filterWorkflows } from '../state/derive.js';

function chips(step) {
  return `
    <div class="chips">
      <span class="chip">Owner: ${step.owner}</span>
      <span class="chip">Module: ${step.module}</span>
    </div>
  `;
}

function renderTimelineCard(step, index) {
  return `
    <article class="timeline-card">
      <div class="meta">
        <strong>Step ${index + 1}</strong>
        <span>${step.evidence}</span>
      </div>
      <h3>${step.title}</h3>
      ${chips(step)}
    </article>
  `;
}

export function populateWorkflowFilter(selectEl, workflows) {
  selectEl.innerHTML = `
    <option value="all">All workflows</option>
    ${workflows.map((wf) => `<option value="${wf.id}">${wf.name}</option>`).join('')}
  `;
}

export function renderTimeline(container, workflows, filter) {
  const filtered = filterWorkflows(workflows, filter);
  container.innerHTML = filtered
    .map(
      (wf) => `
      <article class="timeline-card">
        <div class="meta">
          <div>
            <h3>${wf.name}</h3>
            <small>Risk: ${wf.risk}</small>
          </div>
          <div class="chips">
            <span class="chip">${wf.steps.length} steps</span>
            <span class="chip">${wf.risk.toUpperCase()}</span>
          </div>
        </div>
        <div class="timeline">
          ${wf.steps.map((step, idx) => renderTimelineCard(step, idx)).join('')}
        </div>
      </article>
    `
    )
    .join('');
}
