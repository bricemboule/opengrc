# Cyber GRC Feature Map

This note captures the first-pass extraction of the client's ToR and how it maps to the new `cybergrc` foundation in the product.

## Key Functionalities Extracted From The ToR

### 1. National CII Governance Framework
- National CII protection policy
- CII regulation
- institutional framework
- CII mapping and owner designation
- GIS mapping outputs and raw data
- criticality, vulnerability, and mission assurance assessments

### 2. National Risk Register
- centralized risk database and web application
- CII profiles and owner updates
- risk dashboards
- risk scoring, analysis, owners, and response plans
- continuous risk assessment guideline
- risk training and certification

### 3. National Cyber Contingency Planning
- coordination and communication procedures
- contingency plans and crisis workflows
- information-sharing mechanisms
- emergency response asset prioritization
- SOPs, reporting templates, and review loops
- drills and simulation exercises

### 4. Minimum Standards For ISP And Banking Equipment
- stakeholder engagement plan
- technical committee support
- standards for firmware, authentication, encryption, privacy, backup, DR, and continuity
- conformity assessment and legal review support

### 5. Audit And Protection Of CNI
- stakeholder engagement
- CNI standards
- audit guidelines and compliance framework
- incident response and recovery procedures
- training and awareness

## Foundation Added In The Product

### Backend domain
- `Stakeholder`
- `CriticalInfrastructure`
- `GovernanceArtifact`
- `RiskRegisterEntry`
- `ContingencyPlan`
- `EmergencyResponseAsset`
- `SimulationExercise`
- `CyberStandard`
- `AuditFramework`
- `TrainingProgram`
- `DeliverableMilestone`

### Coverage by phase
- Governance is covered through stakeholders, infrastructure profiles, and governance artifacts.
- Risk management is covered through infrastructure profiles, risk register entries, training programs, and milestones.
- Contingency planning is covered through contingency plans, emergency assets, simulation exercises, and governance artifacts such as SOPs and templates.
- Standards are covered through cyber standards, stakeholder records, and governance artifacts such as SEPs and validation reports.
- Audit and protection are covered through audit frameworks, cyber standards, training programs, and milestones.

## Intentionally Deferred

- menu cleanup to only the client-requested scope
- custom dashboards and visual reporting screens
- deeper workflows such as approval chains, document uploads, and exercise scoring
- richer stakeholder collaboration flows

The current work is meant to give each requested area a solid data and CRUD foundation so we can expand each feature safely in the next iteration.
