import assert from 'node:assert/strict';
import { groupModulesByLayer, filterWorkflows, computeStatusScore } from '../src/state/derive.js';

const sampleModules = [
  { id: 'a', layer: 'one', status: 'healthy' },
  { id: 'b', layer: 'one', status: 'warning' },
  { id: 'c', layer: 'two', status: 'risky' }
];

const sampleWorkflows = [
  { id: 'x', risk: 'low', steps: [] },
  { id: 'y', risk: 'high', steps: [] }
];

const tests = [];

function test(name, fn) {
  tests.push({ name, fn });
}

test('groupModulesByLayer groups modules under their layer key', () => {
  const grouped = groupModulesByLayer(sampleModules);
  assert.equal(grouped.one.length, 2);
  assert.equal(grouped.two.length, 1);
});

test('filterWorkflows filters by workflow id when provided', () => {
  const results = filterWorkflows(sampleWorkflows, { workflowId: 'x', risk: 'all' });
  assert.equal(results.length, 1);
  assert.equal(results[0].id, 'x');
});

test('filterWorkflows filters by risk tier', () => {
  const results = filterWorkflows(sampleWorkflows, { workflowId: 'all', risk: 'high' });
  assert.equal(results.length, 1);
  assert.equal(results[0].id, 'y');
});

test('computeStatusScore calculates average health weight', () => {
  const score = computeStatusScore(sampleModules);
  assert.ok(Math.abs(score - 0.5) < 0.001);
});

let failures = 0;
for (const { name, fn } of tests) {
  try {
    fn();
    console.log(`\u2713 ${name}`);
  } catch (error) {
    failures += 1;
    console.error(`\u2717 ${name}`);
    console.error(error);
  }
}

if (failures > 0) {
  process.exitCode = 1;
}
