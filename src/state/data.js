export const layers = [
  {
    id: 'strategic',
    title: 'Strategic governance',
    summary: 'Sets risk appetite, trust anchors, and mandate templates.',
    tags: ['Mandates', 'Trust registry', 'Standards']
  },
  {
    id: 'tactical',
    title: 'Tactical governance',
    summary: 'Applies domain policies, approval matrices, and escalation paths.',
    tags: ['Approvals', 'Escalation', 'Playbooks']
  },
  {
    id: 'operational',
    title: 'Operational governance',
    summary: 'Runs runbooks, SLO thresholds, and evidence checks through adapters.',
    tags: ['Runbooks', 'SLOs', 'Evidence']
  }
];

export const modules = [
  {
    id: 'policy-engine',
    name: 'Policy Engine',
    layer: 'strategic',
    description: 'Evaluates mandates, policy bundles, and contextual risk.',
    interfaces: ['REST', 'OPA/Rego', 'Pub/Sub'],
    status: 'healthy'
  },
  {
    id: 'mandate-registry',
    name: 'Mandate Registry',
    layer: 'strategic',
    description: 'Canonical store for mandates, templates, and signers.',
    interfaces: ['gRPC', 'SQL'],
    status: 'healthy'
  },
  {
    id: 'workflow-orchestrator',
    name: 'Workflow Orchestrator',
    layer: 'tactical',
    description: 'Routes tasks, orders approvals, and applies run constraints.',
    interfaces: ['REST', 'Queues', 'GraphQL'],
    status: 'warning'
  },
  {
    id: 'risk-scoring',
    name: 'Risk Scoring',
    layer: 'tactical',
    description: 'Scores requests using policy metadata and telemetry baselines.',
    interfaces: ['REST', 'Streams'],
    status: 'healthy'
  },
  {
    id: 'execution-adapter',
    name: 'Execution Adapter',
    layer: 'operational',
    description: 'Integrates CI/CD, data access, or ticketing runtimes.',
    interfaces: ['Webhook', 'CLI', 'SDK'],
    status: 'risky'
  },
  {
    id: 'evidence-lake',
    name: 'Evidence Lake',
    layer: 'operational',
    description: 'Collects attestations, logs, and signed artifacts.',
    interfaces: ['S3', 'SIEM', 'Ledger'],
    status: 'healthy'
  }
];

export const workflows = [
  {
    id: 'deployment',
    name: 'Policy-driven deployment',
    risk: 'medium',
    steps: [
      {
        title: 'Mandate issued',
        owner: 'Strategic',
        module: 'Mandate Registry',
        evidence: 'Signed mandate v1.2'
      },
      {
        title: 'Risk scored',
        owner: 'Tactical',
        module: 'Risk Scoring',
        evidence: 'Score=0.42 / medium'
      },
      {
        title: 'Approvals enforced',
        owner: 'Tactical',
        module: 'Workflow Orchestrator',
        evidence: '2-of-2 approvals logged'
      },
      {
        title: 'Pipeline executed',
        owner: 'Operational',
        module: 'Execution Adapter',
        evidence: 'GitOps hash 8c21, attestations stored'
      },
      {
        title: 'Evidence published',
        owner: 'Operational',
        module: 'Evidence Lake',
        evidence: 'SBOM + run logs archived'
      }
    ]
  },
  {
    id: 'incident',
    name: 'Incident response',
    risk: 'high',
    steps: [
      {
        title: 'Alert triaged',
        owner: 'Tactical',
        module: 'Workflow Orchestrator',
        evidence: 'SEV2 classification'
      },
      {
        title: 'Containment runbook',
        owner: 'Operational',
        module: 'Execution Adapter',
        evidence: 'Access revoked; firewall updated'
      },
      {
        title: 'Postmortem draft',
        owner: 'Strategic',
        module: 'Policy Engine',
        evidence: 'Template pre-filled with evidence links'
      }
    ]
  },
  {
    id: 'data-access',
    name: 'Data access request',
    risk: 'low',
    steps: [
      {
        title: 'Request validated',
        owner: 'Tactical',
        module: 'Policy Engine',
        evidence: 'Data classification: PII-limited'
      },
      {
        title: 'Time-bound access',
        owner: 'Operational',
        module: 'Execution Adapter',
        evidence: 'JIT credentials issued (24h)'
      },
      {
        title: 'Closure + evidence',
        owner: 'Operational',
        module: 'Evidence Lake',
        evidence: 'Access logs & expiry confirmation'
      }
    ]
  }
];
