import { describe, expect, it } from 'vitest';
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

describe('groupModulesByLayer', () => {
  it('groups modules under their layer key', () => {
    const grouped = groupModulesByLayer(sampleModules);
    expect(grouped.one).toHaveLength(2);
    expect(grouped.two).toHaveLength(1);
  });
});

describe('filterWorkflows', () => {
  it('filters by workflow id when provided', () => {
    const results = filterWorkflows(sampleWorkflows, { workflowId: 'x', risk: 'all' });
    expect(results).toHaveLength(1);
    expect(results[0].id).toBe('x');
  });

  it('filters by risk tier', () => {
    const results = filterWorkflows(sampleWorkflows, { workflowId: 'all', risk: 'high' });
    expect(results).toHaveLength(1);
    expect(results[0].id).toBe('y');
  });
});

describe('computeStatusScore', () => {
  it('calculates average health weight', () => {
    const score = computeStatusScore(sampleModules);
    expect(score).toBeCloseTo(0.5);
  });
});
