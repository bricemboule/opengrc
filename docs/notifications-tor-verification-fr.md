# Analyse Des Notifications Au Regard Du ToR

## Objet

Cette note identifie les cas métier pour lesquels des notifications devraient logiquement être émises à partir des exigences du ToR, puis vérifie si la plateforme actuelle les crée réellement.

Ici, le mot "notification" désigne bien ce qui apparaît quand on clique sur l'icône cloche dans l'interface.

## Sources Utilisées

- la synthèse fonctionnelle du ToR déjà consolidée dans `docs/tor-conformite-et-plan-de-test-fr.md`
- le mapping fonctionnel dans `docs/cybergrc-feature-map.md`
- le code de création et diffusion des notifications :
  - `backend/apps/communications/notifications.py`
  - `backend/apps/communications/views.py`
  - `backend/apps/cybergrc/notifications.py`
  - `backend/apps/cybergrc/signals.py`
  - `backend/apps/cybergrc/tasks.py`
- un contrôle de la base PostgreSQL courante sur la table `communications_notification`

## Point Important

Le ToR n'énumère pas forcément, ligne par ligne, chaque notification UI attendue.

Donc l'analyse ci-dessous repose sur une lecture produit raisonnable :

- quand le ToR parle de coordination, suivi, échéances, revue, risque, plan d'urgence, simulation, audit, workflow ou monitoring
- il est logique d'en déduire des cas d'usage de notifications dans la cloche

## Ce Que La Plateforme Appelle Une Notification

La plateforme crée des entrées `communications.Notification` via `dispatch_notification(...)`.

Ensuite :

- ces notifications sont stockées en base
- elles sont poussées en temps réel via websocket
- elles sont lues dans la cloche via `NotificationViewSet`

Donc si un cas n'appelle jamais `dispatch_notification` ou `broadcast_notification`, il ne remontera pas dans la cloche.

## Vérification Rapide Sur La Base Actuelle

Le contrôle de la base courante montre :

- `7` notifications actuellement stockées
- toutes avec `source = cybergrc`
- toutes liées à des consultations de parties prenantes

Exemples réellement présents :

- `Consultation meeting scheduled: First Meeting on 17 Apr 2026 09:00 via in person`
- `Consultation follow-up due: First Meeting on 2026-04-19`
- `Consultation confirmed: First Meeting`

Conclusion immédiate

- certaines notifications sont bien créées et visibles en base
- mais la base actuelle ne prouve pas encore, à elle seule, l'activation de tous les autres cas codés
- pour les autres, on a une preuve code forte mais pas encore une preuve données dans le dataset courant

## Matrice D'Analyse

### 1. Gouvernance, Coordination Et Revues

| Cas métier attendu d'après le ToR | Notification attendue dans la cloche | Implémentation actuelle | Vérifiée dans la base actuelle | Verdict |
|---|---|---|---|---|
| Revue d'un artefact de gouvernance (policy, regulation, guideline, SOP) | Alerte de revue planifiée | Oui, via `notify_review_schedule()` sur `GovernanceArtifact` | Non observée dans les données actuelles | Couverte |
| Transition de workflow sur un artefact de gouvernance | Alerte de changement de statut | Oui, via `notify_workflow_transition()` sur `GovernanceArtifact` | Non observée | Couverte |
| Revue documentaire / desk study avec échéance | Alerte de date prévue ou de statut | Oui, via `notify_due_date()` et workflow sur `DeskStudyReview` | Non observée | Couverte |
| Consultation partie prenante planifiée | Alerte de réunion programmée | Oui, via `notify_consultation_activity()` | Oui | Couverte |
| Suivi post-consultation | Alerte de follow-up dû | Oui, via `notify_consultation_activity()` et `send_consultation_reminders()` | Oui | Couverte |
| Coordination / information sharing entre acteurs | Alerte de coordination métier | Partiellement : couvert pour les consultations et workflows, pas comme moteur générique de collaboration | Partiellement observée via consultations | Partiellement couverte |
| Rappels avant réunion de coordination | Rappel J-1 / avant réunion | Oui, via `send_consultation_reminders()` | Non observée dans la base actuelle | Couverte |

### 2. Risques, Contingence Et Réponse

| Cas métier attendu d'après le ToR | Notification attendue dans la cloche | Implémentation actuelle | Vérifiée dans la base actuelle | Verdict |
|---|---|---|---|---|
| Risque élevé ou critique identifié | Alerte de risque élevé / critique | Oui, via `notify_high_risk()` sur `RiskRegisterEntry` | Non observée | Couverte |
| Date de réponse / traitement d'un risque | Alerte d'échéance opérationnelle | Oui, via `notify_due_date()` sur `RiskRegisterEntry.response_deadline` et notification de transition sur `treatment_status` | Non observée | Couverte |
| Blocage sur plan d'action | Alerte de blocker | Oui, via `notify_action_plan_activity()` | Non observée | Couverte |
| Échéance d'une tâche de remédiation | Alerte de date de tâche | Oui, via `notify_due_date()` sur `ActionPlanTask` | Non observée | Couverte |
| Revue d'un plan d'urgence cyber (Contingency Plan) | Alerte de revue planifiée | Oui, via `notify_plan_activity()` | Non observée | Couverte |
| Changement de statut d'un plan d'urgence | Alerte de workflow | Oui, via `notify_plan_activity()` | Non observée | Couverte |
| Ressources d'urgence (Emergency Response Assets) | Alerte sur indisponibilité, priorité, changement critique | Partiellement : notification de transition sur `EmergencyResponseAsset.availability_status` | Non observée | Partiellement couverte |
| Classification d'incidents | Alerte lors d'un incident classifié / aggravé | Non identifiée | Non | Non couverte |
| Procédures d'escalade (Escalation Procedures) | Alerte d'escalade formalisée | Non identifiée comme moteur dédié | Non | Faiblement couverte |
| Intégration avec systèmes d'urgence externes | Notification depuis ou vers système tiers | Non identifiée | Non | Non couverte |
| Exercice de simulation planifié | Alerte d'exercice prévu | Oui, via `notify_exercise_schedule()` | Non observée | Couverte |

### 3. Cartographie, Standards, Audit, Capacités Et Monitoring

| Cas métier attendu d'après le ToR | Notification attendue dans la cloche | Implémentation actuelle | Vérifiée dans la base actuelle | Verdict |
|---|---|---|---|---|
| Mise à jour du mapping d'une infrastructure critique | Alerte de mapping mis à jour | Oui, via `notify_mapping_progress()` | Non observée | Couverte |
| Mise à jour du statut de désignation CII | Alerte de désignation validée | Oui, via `notify_mapping_progress()` | Non observée | Couverte |
| Gap de capacité élevé / critique | Alerte de gap identifié | Oui, via `notify_capacity_activity()` | Non observée | Couverte |
| Échéance d'une capacity assessment | Alerte d'échéance | Oui, via `notify_due_date()` sur `CapacityAssessment` | Non observée | Couverte |
| Revue d'un standard cyber | Alerte de revue standard | Oui, via `notify_standard_activity()` | Non observée | Couverte |
| Transition de workflow d'un standard cyber | Alerte de changement de statut | Oui, via `notify_standard_activity()` | Non observée | Couverte |
| Revue d'un cadre d'audit | Alerte de revue d'audit | Oui, via `notify_audit_activity()` | Non observée | Couverte |
| Non-conformité ou échec d'audit | Alerte de compliance breach | Non identifiée explicitement | Non | Partiellement couverte |
| Programme de formation changé de statut | Alerte de workflow | Oui, via `notify_training_activity()` | Non observée | Couverte |
| Session de formation planifiée / rappelée | Alerte d'échéance formation | Non identifiée explicitement | Non | Partiellement couverte |
| Livrable proche de l'échéance | Alerte de deadline | Oui, via `notify_deliverable_deadline()` | Non observée | Couverte |
| Monitoring continu des risques | Alerte proactive continue | Partiellement : files d'attention et cockpit existent, mais pas de moteur d'alerting configurable | Non | Partiellement couverte |

## Ce Qui Est Clairement Couvert

Les notifications réellement prises en charge dans le code concernent déjà bien :

- les réunions de consultation planifiées
- les follow-up de consultation
- les rappels de consultation
- les dates de revue
- les dates d'échéance
- les transitions de workflow
- les transitions de workflow sur les modules Cyber GRC principaux
- les risques élevés / critiques
- les échéances de réponse au risque
- les exercices planifiés
- les livrables à échéance
- les gaps de capacité élevés / critiques
- les blockages de plan d'action
- les changements de mapping / désignation d'infrastructures

## Ce Qui Est Seulement Partiel

Les sujets suivants sont seulement couverts de façon indirecte ou incomplète :

- partage d'information et coordination nationale avancée
- gestion des réponses au risque via chaîne complète de remédiation
- alertes de conformité métier
- planification et rappels de formation
- monitoring continu mature

## Ce Qui Manque Vraiment Pour Les Notifications

Je n'ai pas trouvé de notifications explicites pour :

- les ressources d'urgence `Emergency Response Assets`
- une vraie logique d'escalade opérationnelle
- la classification d'incidents
- les sanctions / pénalités réglementaires
- l'intégration avec des systèmes d'urgence externes
- une allocation de ressources outillée par alertes

## Verdict Global

Si on parle strictement des notifications visibles dans la cloche :

- la plateforme couvre déjà correctement les notifications de suivi opérationnel et de coordination de base
- elle couvre bien les échéances, revues, statuts, consultations, risques élevés et blocages
- elle ne couvre pas encore complètement les notifications plus stratégiques ou institutionnelles attendues par une plateforme nationale mature

Autrement dit :

- pour un MVP Cyber GRC, la couverture notifications est déjà crédible
- pour une conformité forte au ToR, il reste un deuxième niveau à construire

## Recommandation Produit

Si vous voulez rapprocher davantage la plateforme de l'esprit du ToR, les prochaines notifications à ajouter en priorité seraient :

1. alertes d'escalade opérationnelle
2. alertes d'incident classifié / aggravé
3. alertes sur indisponibilité des ressources d'urgence
4. alertes de non-conformité / audit failure
5. rappels et échéances de formation
6. alertes de monitoring continu configurables
