# Nicole Protocol

The Nicole Protocol is a recursive governance framework for orchestrating human and machine stakeholders through modular layers. It formalizes decision-making, accountability, and execution flows so distributed teams can compose reliable automation while retaining transparent oversight.

## Purpose and Vision
- **Interoperable governance:** Provide a common vocabulary for policy, execution, and oversight that can be embedded into diverse projects.
- **Composable modules:** Enable teams to swap or extend governance components (policy, agents, audits) without rewriting the entire system.
- **Traceable automation:** Ensure every automated action is backed by explicit mandates, logged evidence, and clear ownership.
- **Human-in-the-loop:** Balance autonomous execution with review checkpoints and escalation paths.

## Core Concepts
- **Mandates:** Structured intents combining objective, scope, constraints, and accountability owners.
- **Layers:** Governance, control, and execution layers cascade responsibilities from policy to action.
- **Modules:** Reusable building blocks (identity, policy engines, schedulers, auditors) that implement layer duties.
- **Evidence Trails:** Signed logs and artifacts that demonstrate compliance with mandates and reviews.
- **Escalation Paths:** Defined routes for exception handling and human approvals.

## Architecture Overview
1. **Governance Layer (Policy & Direction)**
   - Defines mandates, standards, risk thresholds, and approval matrices.
   - Maintains registries for roles, permissions, and trust anchors.
   - Publishes policy APIs consumed by downstream control modules.
2. **Control Layer (Coordination & Assurance)**
   - Translates governance rules into actionable workflows.
   - Performs validation, scheduling, and conflict resolution.
   - Routes tasks to execution modules and enforces review checkpoints.
3. **Execution Layer (Action & Feedback)**
   - Runs playbooks, agents, or services that fulfill mandates.
   - Emits telemetry, status updates, and evidence artifacts.
   - Feeds results back to control and governance for audits.

## Module Responsibilities
- **Identity & Trust:** Role registry, credential verification, key management.
- **Policy Engine:** Mandate parsing, policy evaluation, exception handling.
- **Workflow Orchestrator:** Task routing, dependency management, retry logic.
- **Execution Adapters:** Integrations to CI/CD, ticketing, data pipelines, or agent runtimes.
- **Audit & Observability:** Evidence collection, attestations, dashboards, and anomaly alerts.
- **Storage & State:** Mandate store, run history, evidence vaults, configuration snapshots.

## Governance Layers in Detail
- **Strategic Governance:** Vision, risk appetite, and cross-domain standards; owns mandate templates and trust anchors.
- **Tactical Governance:** Domain playbooks, approval matrices, and escalation policies; curates control-layer workflows.
- **Operational Governance:** Runbooks, SLO/SLA thresholds, observability requirements; interfaces with execution adapters.

## Setup Requirements
- **Runtime:** Python 3.11+ and Node.js 18+ for reference SDKs and UI modules.
- **Tooling:** Git, Make, and Docker (optional) for isolated environments.
- **Secrets:** Configure signing keys and credential stores (e.g., Vault) for identity modules.
- **Environment Variables:**
  - `NICOLE_ENV` (e.g., `dev`, `staging`, `prod`)
  - `NICOLE_POLICY_STORE` (URI for mandate/policy backend)
  - `NICOLE_EVIDENCE_STORE` (URI for logs/artifacts)

## Running Locally
1. **Install dependencies** (example using Make):
   ```bash
   make install
   ```
2. **Start core services** (policy, orchestrator, adapters):
   ```bash
   make start
   ```
3. **Run a sample mandate** through the control layer:
   ```bash
   make demo
   ```
4. **Inspect evidence** emitted by the execution layer:
  ```bash
  make logs
  ```

### Modular UI console (where to find it)
- Source files live under `src/` with `index.html` at the repository root; building copies everything into `dist/` for static hosting.
- It runs on native ES modules with zero external dependencies (no backend required) and can be extended with live data sources.

Run it locally from source:
```bash
npm run dev      # static dev server on port 5173, serving the repo root
```

Build and preview the static bundle (served from `dist/`):
```bash
npm run build    # copy index.html and src/ into dist/
npm run preview  # serve the built assets from dist/ on port 5173
```

Key UI regions:
- **Governance layers**: shows the strategic → tactical → operational stack with responsibilities.
- **Modules**: cards for policy engines, orchestrators, adapters, and evidence stores with interface metadata and health.
- **Workflow simulator**: filterable timelines (by workflow and risk) to trace mandate execution and evidence.

## Documentation Site / Build Status
- This repository currently ships the protocol reference as Markdown only; no site bundle or app build is committed.
- To publish the documentation as a website, pick a static site generator (e.g., MkDocs, Docusaurus, or Next.js) and wire it to the existing Markdown.
- Example MkDocs flow (once a `mkdocs.yml` and `docs/` tree are added):
  ```bash
  pip install mkdocs mkdocs-material
  mkdocs serve   # local preview
  mkdocs build   # generate static site
  ```
- Example Next.js flow (once a `/site` app exists):
  ```bash
  cd site
  npm install
  npm run dev    # local preview
  npm run build  # static export or server build
  ```
- CI/CD recommendation: add a job that runs the chosen build command and publishes the output (e.g., GitHub Pages or a static bucket).

## Testing and Validation
- **UI/state logic tests (Node-only harness):**
  ```bash
  npm test
  ```
  Runs the lightweight assertions in `test/derive.test.js` without external dependencies.
- **Static bundle build:**
  ```bash
  npm run build
  ```
  Copies `index.html` and the `src/` tree into `dist/` for static hosting.
- **Local preview server:**
  ```bash
  npm run dev
  ```
  Starts a zero-dependency static server on port 5173. Open `http://localhost:5173` to explore the modular console.

## Integration Patterns
- **API-first:** Consume the governance and control APIs to submit mandates, query status, or fetch evidence.
- **Adapter model:** Implement execution adapters that conform to the orchestration contract (inputs: mandate context; outputs: status + evidence).
- **Webhooks/Events:** Subscribe to lifecycle events (submitted, approved, running, completed, escalated) to trigger external systems.
- **Policy as Code:** Store mandates and policies in version control; use CI checks to validate before deployment.

## Example Workflows
### Policy-driven deployment
1. Strategic governance defines deployment mandate templates with risk tiers.
2. Control layer validates an incoming deployment request, runs checks, and requires approvals for high-risk changes.
3. Execution adapters run CI/CD pipelines; evidence is signed and sent back to the audit module.
4. Governance dashboard displays compliance status and escalation history.

### Incident response
1. Tactical governance publishes incident runbooks and escalation matrices.
2. Control layer triggers incident workflows based on alerts and routes tasks to responders.
3. Execution adapters coordinate communications, ticketing, and containment actions.
4. Audit module aggregates timelines, evidence, and postmortem inputs.

### Data access request
1. Strategic governance sets data classification policies.
2. Control layer evaluates access mandates against policies and risk scoring.
3. Execution adapters provision access with time-bound credentials.
4. Evidence and expirations are logged; renewal or revocation follows policy.

## Contribution Guidelines
- **Branching:** Use feature branches; keep commits scoped and descriptive.
- **Standards:** Follow policy, adapter, and workflow contract definitions; add tests for new modules.
- **Reviews:** Require at least one reviewer for governance-affecting changes; include mandate/evidence examples in PRs.
- **Documentation:** Update diagrams, configuration samples, and runbooks alongside code changes.
- **Security:** Never commit secrets; rotate keys and verify signatures for evidence-producing components.

## Licensing Notes
The Nicole Protocol is distributed under the [MIT License](LICENSE). Contributions are accepted under the same license. Ensure third-party modules comply with MIT-compatible terms and document any additional notices in `NOTICE` files.

## Roadmap (high level)
- Reference SDKs for policy and control APIs.
- Pluggable evidence backends (object storage, ledger, SIEM).
- Governance dashboards with lineage visualization.
- Automated conformity checks for mandate templates and adapters.
