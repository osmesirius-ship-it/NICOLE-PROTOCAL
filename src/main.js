import { layers, modules, workflows } from './state/data.js';
import { groupModulesByLayer, computeStatusScore } from './state/derive.js';
import { renderLayers } from './components/layers.js';
import { renderModules } from './components/modules.js';
import { populateWorkflowFilter, renderTimeline } from './components/workflows.js';
import './style.css';

const layerGrid = document.getElementById('layer-grid');
const moduleGrid = document.getElementById('module-grid');
const timelineEl = document.getElementById('workflow-timeline');
const workflowFilterEl = document.getElementById('workflow-filter');
const riskFilterEl = document.getElementById('risk-filter');

function render() {
  renderLayers(layerGrid, layers);
  renderModules(moduleGrid, modules);
  renderTimeline(timelineEl, workflows, {
    workflowId: workflowFilterEl.value,
    risk: riskFilterEl.value
  });
}

function hydrateMeta() {
  const score = computeStatusScore(modules);
  document.title = `Nicole Console · Health ${score}`;
}

function attachEvents() {
  workflowFilterEl.addEventListener('change', render);
  riskFilterEl.addEventListener('change', render);
  document.getElementById('reset-layout').addEventListener('click', () => {
    workflowFilterEl.value = 'all';
    riskFilterEl.value = 'all';
    render();
  });
  document.getElementById('refresh-data').addEventListener('click', () => {
    render();
  });
}

populateWorkflowFilter(workflowFilterEl, workflows);
hydrateMeta();
attachEvents();
render();
