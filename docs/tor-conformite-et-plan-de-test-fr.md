# Matrice De Conformité ToR Et Plan De Test

## Objet

Ce document évalue dans quelle mesure la plateforme actuelle répond aux exigences métier extraites du ToR, puis propose un plan de test fonctionnel en français pour vérifier cette couverture.

L'analyse est basée sur l'implémentation actuelle du produit, notamment :

- le mapping fonctionnel dans `docs/cybergrc-feature-map.md`
- les modules et champs configurés dans `frontend/src/config/modules.js`
- les vues supplémentaires et workflows dans `frontend/src/config/moduleBehaviors.js`
- les modèles métier dans `backend/apps/cybergrc/models.py`
- le cockpit de pilotage dans `backend/apps/cybergrc/views.py` et `frontend/src/pages/DashboardPage.jsx`

## Légende D'Évaluation

| Statut | Signification |
|---|---|
| Couverte | La plateforme implémente déjà la fonctionnalité de façon explicite et exploitable |
| Partiellement couverte | La base existe mais la couverture reste incomplète, indirecte, ou trop légère |
| Faiblement couverte | Un embryon existe mais ne suffit pas à considérer l'exigence comme réellement adressée |
| Non couverte | Aucun élément probant n'a été identifié dans l'état actuel |

## Hypothèse Importante

L'évaluation porte sur la plateforme telle qu'elle existe aujourd'hui comme produit applicatif.

Cela signifie que :

- un besoin peut être "couvert" au niveau structure produit sans être encore "déployé nationalement"
- les intégrations externes, l'exploitation institutionnelle, les sanctions juridiques, ou les connexions temps réel avec des systèmes tiers ne sont pas considérées comme acquises sauf si elles sont visibles dans le produit

## Matrice De Conformité

### 1. Gouvernance Et Cartographie

| ID | Exigence | Couverture | Preuve principale | Gap principal |
|---|---|---|---|---|
| R1 | Cadre national de cybersécurité (Cybersecurity Management Framework) | Partiellement couverte | `Governance Artifacts`, `Stakeholders`, `Critical Infrastructure`, `Deliverable Milestones` | Le cadre institutionnel complet reste surtout modélisé |
| R2 | Politique nationale de protection CII (National CII Protection Policy) | Couverte | module `Governance Artifacts`, types `policy`, `regulation`, `guideline`, `framework`, `sop`, `template` | Pas de validation institutionnelle externe visible |
| R3 | Cadre institutionnel (Institutional Framework) | Partiellement couverte | `Stakeholders`, `Stakeholder Consultations`, `Desk Study Reviews` | Pas de matrice RACI ou gouvernance formelle dédiée |
| R4 | Régulations cybersécurité (Cybersecurity Regulations) | Partiellement couverte | artefacts `regulation`, workflows, reports, review dates | Sanctions, pénalités et juridique détaillé non outillés |
| R5 | Classification des infrastructures | Couverte | `infrastructure_type`, `designation_status`, `criticality_level`, `vulnerability_level` | Bonne base fonctionnelle |
| R9 | Cartographie des infrastructures critiques (CII Mapping) | Couverte | `Critical Infrastructure`, `GIS map`, `Coverage report`, dashboard map | Très bien couvert dans le MVP |
| R10 | Propriétaires des actifs (owners) | Couverte | `owner_stakeholder`, `owner_name` | Couverture claire |
| R11 | Évaluation de criticité (Criticality Assessment) | Couverte | `criticality_level` | Couvert |
| R12 | Évaluation des vulnérabilités (Vulnerability Assessment) | Couverte | `vulnerability_level`, `risk_summary` | Couvert à un niveau déclaratif |
| R13 | Cartographie géospatiale (GIS Mapping) | Couverte | carte interactive, points, couverture | Couvert |
| R14 | Données brutes, dashboards, cartes | Couverte | `DashboardPage`, `MapView`, reports | Bien couvert |

### 2. Risques Et Capacités

| ID | Exigence | Couverture | Preuve principale | Gap principal |
|---|---|---|---|---|
| R6 | Scoring des risques | Couverte | `likelihood`, `impact`, `risk_score`, `risk_level` | Le moteur analytique avancé n'est pas visible |
| R15 | Base de données des risques (Risk Register / Risk Database) | Couverte | `RiskRegisterEntry`, workflow, report | Très bien couvert comme socle |
| R16 | Analyse probabilité + impact | Couverte | `likelihood`, `impact`, `risk_score` | Couvert |
| R17 | Mises à jour par les acteurs | Partiellement couverte | CRUD complet, reports, listes, formulaires | Pas de validation multi-acteurs avancée |
| R18 | Accès web (Web Application) | Couverte | listes, création, édition, report, map, calendar, dashboard | Couvert |
| R19 | Intégration avec systèmes d'urgence (Emergency Response Systems) | Faiblement couverte | lien fonctionnel avec `Contingency Plans` et `Emergency Response Assets` | Pas d'intégration technique externe visible |
| R20 | Guidelines de gestion des risques (Risk Management Guidelines) | Partiellement couverte | `Governance Artifacts` + `Risk Register` + `Capacity Assessments` | Couverture éclatée, pas de module méthodologique dédié |
| R21 | Identification des risques (Risk Identification) | Couverte | titre, catégorie, infrastructure, owner | Couvert |
| R22 | Modélisation des menaces (Threat Modelling) | Faiblement couverte | possible via `scenario` ou `category` | Pas de champ explicite `threat model` |
| R23 | Scénarios de risques (Risk Scenarios) | Couverte | champ `scenario` | Couvert |
| R24 | Analyse et priorisation | Couverte | score, niveau, distribution, risques critiques | Couvert |
| R25 | Stratégies de réponse (Risk Response) | Couverte | `response_plan`, `response_deadline`, `Action Plan Tasks` | Couvert |
| R26 | Formation des acteurs (Training Programs) | Couverte | type, audience, mode, certification, statut | Couvert |

### 3. Contingence, Coordination Et Simulation

| ID | Exigence | Couverture | Preuve principale | Gap principal |
|---|---|---|---|---|
| R7 | Procédures d'escalade (Escalation Procedures) | Faiblement couverte | workflows, deadlines, `Attention queue` | Pas de moteur d'escalade configurable |
| R8 | Gestion des incidents (Incident Response) | Partiellement couverte | `Contingency Plans`, `Audit Frameworks`, `Emergency Response Assets` | Couverture surtout procédurale |
| R27 | Plan d'urgence cyber (Cyber Contingency Plan) | Couverte | type, statut, coordination, partage d'info, déclencheurs | Bien couvert comme structure |
| R28 | Priorités des ressources (Emergency Response Assets) | Couverte | type d'actif, priorité, disponibilité, propriétaire | Couvert |
| R29 | Procédures opérationnelles (Standard Operating Procedures - SOPs) | Couverte | type `sop` dans `Governance Artifacts` | Couvert |
| R30 | Classification des incidents | Partiellement couverte | `Contingency Plans`, `Audit Frameworks`, `Desk Study Reviews` | Pas de taxonomie incident dédiée |
| R31 | Mécanismes de coordination (Coordination Mechanisms) | Partiellement couverte | consultations, `coordination_mechanism`, calendar, workflow | Pas de moteur de collaboration temps réel avancé |
| R32 | Partage d'information (Information Sharing) | Partiellement couverte | `information_sharing_protocol`, consultations | Procédural plus que technique |
| R33 | Exercices de simulation (Simulation Exercises) | Couverte | type, scénario, findings, lessons learned | Couvert |
| R34 | Tests de crise (Crisis Testing) | Couverte | simulations, workflows, reports | Couvert au niveau applicatif |
| R35 | Plateformes digitales (Digital Platforms) | Couverte | dashboard, liste, report, map, workflow, calendar | Couvert |
| R36 | Outils d'aide à la décision (Decision Support Systems) | Partiellement couverte | dashboard, priority mix, attention queue, review queue | Pas encore un DSS avancé ou prescriptif |
| R37 | Communication en temps réel | Partiellement couverte | notifications socket, calendar, dashboard alerts | Temps réel présent mais limité |
| R38 | Allocation de ressources | Partiellement couverte | `Emergency Response Assets`, `Action Plan Tasks`, `Deliverable Milestones` | Pas de moteur d'allocation automatique |

### 4. Standards, Audit, Monitoring Et Livraison

| ID | Exigence | Couverture | Preuve principale | Gap principal |
|---|---|---|---|---|
| R39 | Standards de sécurité ISP / banques (Security Standards) | Couverte | `Cyber Standards`, types `isp_equipment`, `banking_equipment`, `control_focus` | Couvert |
| R40 | Chiffrement (Encryption), authentification forte (Strong Authentication), firmware | Partiellement couverte | `control_focus`, `summary` dans `Cyber Standards` | Contrôles gérés comme contenu textuel |
| R41 | Audit & conformité | Couverte | `Audit Frameworks`, `compliance_focus`, `incident_response_procedure`, `recovery_procedure` | Couvert |
| R42 | Respect des standards | Partiellement couverte | lien `related_standard`, reports | Contrôle métier oui, preuve automatisée non visible |
| R43 | Monitoring continu (Risk Monitoring) | Partiellement couverte | `Attention queue`, `Critical risks`, `Review queue`, `Priority mix` | Pas de monitoring continu avancé ni alerting configurable |
| R44 | Documentation, templates, procédures, guides | Couverte | `Governance Artifacts`, `Deliverable Milestones` | Couvert |
| R45 | Workflows multi-acteurs | Couverte | `moduleBehaviors`, `WorkflowBoard`, `Operational matrix` | Couvert |
| R46 | Coordination multi-vues | Couverte | list, report, workflow, map, calendar | Très bon niveau pour le MVP |

## Synthèse De Conformité

### Ce qui est clairement bien couvert

- cartographie des infrastructures critiques (CII Mapping)
- registre des risques (Risk Register / Risk Database)
- analyse et priorisation des risques
- plans d'urgence (Cyber Contingency Plan)
- exercices de simulation (Simulation Exercises)
- standards de sécurité (Security Standards)
- audit et conformité (Audit Framework)
- formations (Training Programs)
- documentation et livrables
- workflows et cockpit de pilotage

### Ce qui est présent mais encore partiel

- cadre institutionnel complet
- procédures d'escalade (Escalation Procedures)
- partage d'information opérationnel avancé
- communication temps réel riche
- aide à la décision avancée
- monitoring continu mature
- allocation de ressources automatisée
- intégration avec systèmes d'urgence externes
- modélisation explicite des menaces (Threat Modelling)

### Verdict Global

La plateforme répond déjà de manière solide à la vision d'une **plateforme nationale de gestion des risques cyber et des infrastructures critiques (National Cyber Risk Management Platform)**.

En revanche, elle doit encore être renforcée si l'on veut affirmer qu'elle couvre intégralement :

- la profondeur réglementaire
- la collaboration nationale multi-acteurs avancée
- les intégrations temps réel et systèmes externes
- la formalisation détaillée de certaines méthodes comme le **Threat Modelling**

## Plan De Test Fonctionnel

## Objectif Du Plan De Test

Vérifier de manière méthodique que les exigences extraites du ToR sont bien prises en compte dans la plateforme actuelle.

## Préconditions Générales

| Élément | Précondition |
|---|---|
| Environnement | L'application tourne en local sans Docker |
| Accès | Un utilisateur administrateur est connecté |
| Données | Les jeux de démo sont chargés |
| Front | Les modules Cyber GRC sont visibles dans le menu |
| Back | Les APIs des modules sont accessibles |

## Cas De Test Détaillés

### 1. Tests Gouvernance Et Cartographie

| ID Test | Module / page | Vérification | Résultat attendu | Verdict |
|---|---|---|---|---|
| TC-01 | `/modules/governance-artifacts` | Créer un artefact `Policy` avec phase, résumé, revue | L'artefact est créé et visible en liste | Conforme / Non conforme |
| TC-02 | `/modules/governance-artifacts` | Créer un artefact `Regulation` puis vérifier report et workflow | La régulation suit un cycle de gestion | Conforme / Partiel |
| TC-03 | `/modules/governance-artifacts` | Créer des artefacts `SOP` et `Template` | Les procédures et modèles sont gérables | Conforme / Non conforme |
| TC-04 | `/modules/cyber-stakeholders` | Créer plusieurs acteurs de types différents | Les parties prenantes sont structurées | Conforme / Partiel |
| TC-05 | `/modules/critical-infrastructure` | Créer une infrastructure avec coordonnées et statut de mapping | L'élément apparaît en liste | Conforme / Non conforme |
| TC-06 | `/modules/critical-infrastructure?mode=map` | Vérifier l'apparition du point sur la carte | Le point est affiché, cliquable et visible sur la carte | Conforme / Non conforme |
| TC-07 | `/modules/critical-infrastructure?mode=report` | Vérifier le report de couverture | Les actifs mappés et non mappés sont exploitables | Conforme / Partiel |
| TC-08 | `/modules/critical-infrastructure?mode=create` | Remplir `criticality_level` et `vulnerability_level` | Les valeurs sont sauvegardées et visibles | Conforme / Non conforme |

### 2. Tests Risques Et Capacités

| ID Test | Module / page | Vérification | Résultat attendu | Verdict |
|---|---|---|---|---|
| TC-09 | `/modules/risk-register` | Créer un risque avec titre, scénario, probabilité, impact, score | Le risque est créé et listé | Conforme / Non conforme |
| TC-10 | `/modules/risk-register` | Vérifier les champs d'analyse de risque | Probabilité, impact, score et niveau sont disponibles | Conforme / Non conforme |
| TC-11 | `/modules/risk-register?mode=report` | Vérifier la remontée des risques prioritaires | Les risques critiques ressortent | Conforme / Partiel |
| TC-12 | `/modules/risk-register` | Renseigner `response_plan` et `response_deadline` | La réponse au risque est persistée | Conforme / Non conforme |
| TC-13 | `/modules/action-plan-tasks` | Créer une tâche liée à un risque | Le lien risque vers action est visible | Conforme / Non conforme |
| TC-14 | `/modules/risk-register` | Rechercher un champ explicite de `Threat Modelling` | Si absent, couverture partielle | Partiel attendu |
| TC-15 | `/modules/risk-register` | Vérifier le champ `scenario` | Les scénarios sont capturés | Conforme / Non conforme |
| TC-16 | `/modules/governance-artifacts` | Créer un artefact `Guideline` de phase `Risk` | Une guideline de gestion des risques peut être créée | Conforme / Partiel |
| TC-17 | `/modules/capacity-assessments` | Créer une évaluation avec maturité, gaps et actions | Les écarts de capacité sont suivis | Conforme / Non conforme |
| TC-18 | `/modules/training-programs` | Créer un programme `Risk management` ou `Standards compliance` | Le programme est visible et rapportable | Conforme / Non conforme |

### 3. Tests Contingence, Coordination Et Simulation

| ID Test | Module / page | Vérification | Résultat attendu | Verdict |
|---|---|---|---|---|
| TC-19 | `/modules/contingency-plans` | Créer un plan avec coordination, partage d'information, déclencheur | Le plan est complet et sauvegardé | Conforme / Non conforme |
| TC-20 | `/modules/emergency-response-assets` | Créer un asset lié à un plan avec priorité et disponibilité | L'actif est traçable et lié au plan | Conforme / Non conforme |
| TC-21 | `/modules/simulation-exercises` | Créer un exercice avec scénario, findings, lessons learned | L'exercice est exploitable de bout en bout | Conforme / Non conforme |
| TC-22 | `/modules/stakeholder-consultations` | Créer une consultation, vérifier workflow, report et calendar | La coordination est visible en plusieurs vues | Conforme / Non conforme |
| TC-23 | `/modules/stakeholder-consultations?mode=calendar` | Vérifier affichage mensuel, horaires, follow-up | Les événements sont visibles au bon mois et à la bonne heure | Conforme / Non conforme |
| TC-24 | `/modules/desk-study-reviews` | Créer une revue documentaire avec gaps et recommandations | L'analyse documentaire est suivie | Conforme / Non conforme |

### 4. Tests Standards, Audit, Livraison Et Cockpit

| ID Test | Module / page | Vérification | Résultat attendu | Verdict |
|---|---|---|---|---|
| TC-25 | `/modules/cyber-standards` | Créer un standard `ISP equipment` puis `Banking equipment` | Les standards sectoriels sont gérés | Conforme / Non conforme |
| TC-26 | `/modules/cyber-standards` | Renseigner `control_focus` et `summary` avec encryption, MFA, firmware | Les exigences de contrôle sont documentées | Conforme / Partiel |
| TC-27 | `/modules/audit-frameworks` | Créer un cadre d'audit lié à un standard | L'audit est lié à la conformité | Conforme / Non conforme |
| TC-28 | `/modules/audit-frameworks` | Renseigner `incident_response_procedure` et `recovery_procedure` | Les procédures existent et sont sauvegardées | Conforme / Non conforme |
| TC-29 | `/modules/deliverable-milestones` | Créer un milestone avec phase, catégorie, statut, échéance | Les livrables sont suivis | Conforme / Non conforme |
| TC-30 | `/dashboard` | Vérifier workflow matrix, alerts, risks, mapping, queues | Le tableau de bord agrège les signaux clés | Conforme / Partiel |
| TC-31 | `/dashboard` | Vérifier attention queue, priority mix, critical risks | Le cockpit fournit un appui à la décision | Conforme / Partiel |
| TC-32 | `/dashboard` et reports | Vérifier l'alimentation des files d'attention | Si les données alimentent dashboard/report, couverture partielle | Partiel attendu |
| TC-33 | `/modules/governance-artifacts` et `/modules/deliverable-milestones` | Vérifier la gestion des reports, templates, guides, procédures | La documentation projet est gérable | Conforme / Non conforme |
| TC-34 | vues `?mode=workflow` | Vérifier lanes, transitions, statuts, indicateurs | Les workflows sont opérationnels | Conforme / Non conforme |
| TC-35 | vues `?mode=report` | Vérifier review queue, due dates, états, distribution | Les vues de reporting existent et sont utiles | Conforme / Non conforme |

## Recette Spécifique Demandée : Risk Management Guidelines

L'objectif ici est de vérifier si la plateforme prend en compte l'exigence suivante :

Créer des **guidelines de gestion des risques (Risk Management Guidelines)** incluant :

- identification des risques (Risk Identification)
- modélisation des menaces (Threat Modelling)
- scénarios de risques (Risk Scenarios)
- analyse et priorisation
- stratégies de réponse (Risk Response)

### Sous-plan De Test Dédié

| ID | Sous-exigence | Où tester | Étapes | Résultat attendu | Évaluation attendue |
|---|---|---|---|---|---|
| RG-01 | Guideline formelle | `/modules/governance-artifacts?mode=create` | Créer un artefact de type `Guideline` pour la phase `Risk` | La guideline est créée | Conforme |
| RG-02 | Risk Identification | `/modules/risk-register?mode=create` | Créer un risque avec titre, infrastructure, catégorie | Le risque est identifiable et stocké | Conforme |
| RG-03 | Threat Modelling | `/modules/risk-register?mode=create` | Vérifier l'existence d'un champ explicite pour les menaces | Aucun champ dédié identifié | Partiel |
| RG-04 | Risk Scenarios | `/modules/risk-register?mode=create` | Renseigner le champ `scenario` | Le scénario est enregistré | Conforme |
| RG-05 | Analyse | `/modules/risk-register?mode=create` | Renseigner `likelihood`, `impact`, `risk_score` | L'analyse est possible | Conforme |
| RG-06 | Priorisation | `/modules/risk-register?mode=report` | Vérifier la mise en avant des niveaux de risque | Le niveau de priorité est visible | Conforme |
| RG-07 | Risk Response | `/modules/risk-register?mode=create` | Renseigner `response_plan` et `response_deadline` | La réponse est documentée | Conforme |
| RG-08 | Exécution de la réponse | `/modules/action-plan-tasks?mode=create` | Créer une tâche liée à un risque | La réponse peut être transformée en plan d'action | Conforme |
| RG-09 | Boucle de revue | `/modules/risk-register?mode=report` + `/dashboard` | Vérifier review, échéance, criticité, dashboard | La boucle de suivi existe | Partiel à Conforme |

### Conclusion Sur Cette Exigence

La plateforme prend bien en compte une large partie de l'exigence **Risk Management Guidelines**, mais avec cette nuance :

- **bien couverts** : identification, scénarios, analyse, priorisation, réponse
- **partiellement couvert** : threat modelling explicite
- **correctement outillé** : déclinaison de la réponse en tâches d'action

## Proposition De Méthode De Recette

Pour exécuter cette recette de façon sérieuse, il est recommandé de suivre cette méthode :

| Étape | Action |
|---|---|
| 1 | Vérifier d'abord la présence du module correspondant dans le menu |
| 2 | Vérifier que la vue liste fonctionne |
| 3 | Vérifier que la création fonctionne |
| 4 | Vérifier que les données créées réapparaissent en liste |
| 5 | Vérifier les vues additionnelles : workflow, report, map, calendar selon le cas |
| 6 | Vérifier la remontée éventuelle sur le dashboard |
| 7 | Classer le verdict en `Conforme`, `Partiel`, `Non conforme` |
| 8 | Noter le gap exact si la couverture est partielle |

## Grille De Verdict Recommandée

| Verdict | Signification |
|---|---|
| Conforme | L'exigence est clairement prise en compte et testable dans la plateforme |
| Partiel | L'exigence existe, mais seulement en partie ou de manière indirecte |
| Non conforme | L'exigence n'est pas réellement visible dans la plateforme |
| À approfondir | Il faudrait une vérification technique ou métier supplémentaire |

## Conclusion Exécutable

Si l'objectif est de démontrer que la plateforme répond déjà au ToR, alors la conclusion défendable est la suivante :

> La plateforme couvre déjà le noyau fonctionnel attendu pour une **plateforme nationale de gestion des risques cyber et des infrastructures critiques (National Cyber Risk Management Platform)**, avec une couverture forte sur la gouvernance documentaire, le registre des risques, la cartographie, les plans de contingence, les standards, les audits, la formation, les workflows et les tableaux de bord.

> En revanche, certaines attentes du ToR restent seulement partiellement couvertes, notamment la **modélisation des menaces (Threat Modelling)** explicite, les **procédures d'escalade (Escalation Procedures)** formalisées, le **monitoring continu (Risk Monitoring)** avancé, l'**allocation de ressources (Resource Allocation)** outillée, et l'intégration avec des systèmes externes d'urgence.

## Recommandation

Avant de conclure définitivement vis-à-vis du client, il faut exécuter la recette ci-dessus et produire une version annotée avec :

- le verdict réel par test
- des captures d'écran
- les écarts constatés
- les priorités de correction
