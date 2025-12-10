export function groupModulesByLayer(modules) {
  return modules.reduce((acc, mod) => {
    if (!acc[mod.layer]) acc[mod.layer] = [];
    acc[mod.layer].push(mod);
    return acc;
  }, {});
}

export function filterWorkflows(workflows, filter) {
  const { workflowId = 'all', risk = 'all' } = filter;
  return workflows.filter((wf) => {
    const byId = workflowId === 'all' || wf.id === workflowId;
    const byRisk = risk === 'all' || wf.risk === risk;
    return byId && byRisk;
  });
}

export function computeStatusScore(modules) {
  const weights = { healthy: 1, warning: 0.5, risky: 0 };
  const total = modules.reduce((sum, mod) => sum + (weights[mod.status] ?? 0), 0);
  return Number((total / modules.length).toFixed(2));
}
