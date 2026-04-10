from pathlib import Path
import textwrap, json

base = Path('/mnt/data/relief_ext')
backend = base/'backend'
frontend = base/'frontend'

APPS = {
    'alerts': [('Alert',[('code','char_unique'),('title','char'),('status','status')]),('CapMessage',[('alert','fk:Alert'),('identifier','char_unique'),('headline','char'),('scope','char_default:public')])],
    'assets': [('AssetType',[('code','char_unique'),('name','char'),('status','status')]),('Asset',[('asset_type','fk:AssetType'),('code','char_unique'),('name','char'),('status','status')]),('Assignment',[('asset','fk:Asset'),('assignee','fk:people.Person:null'),('assigned_to_name','char_blank'),('status','status')])],
    'budgets': [('BudgetPlan',[('code','char_unique'),('name','char'),('status','status')]),('BudgetLine',[('budget_plan','fk:BudgetPlan'),('code','char_unique'),('name','char'),('amount','decimal')])],
    'case_management': [('Client',[('person','fk:people.Person'),('code','char_unique'),('name','char'),('status','status')]),('CaseFile',[('client','fk:Client'),('case_number','char_unique'),('name','char'),('status','status')]),('CaseEvent',[('case_file','fk:CaseFile'),('event_type','char'),('status','status')])],
    'content': [('Page',[('code','char_unique'),('title','char'),('status','status')]),('Post',[('code','char_unique'),('title','char'),('status','status')]),('NewsItem',[('code','char_unique'),('title','char'),('status','status')])],
    'documents': [('Document',[('code','char_unique'),('title','char'),('status','status')]),('FileAttachment',[('document','fk:Document'),('name','char'),('status','status')])],
    'epidemiology': [('EpidemiologyCase',[('code','char_unique'),('name','char'),('status','status')]),('ContactTrace',[('epidemiology_case','fk:EpidemiologyCase'),('name','char'),('status','status')]),('Outbreak',[('code','char_unique'),('name','char'),('status','status')])],
    'events': [('Event',[('code','char_unique'),('title','char'),('status','status')]),('Scenario',[('event','fk:Event'),('name','char'),('status','status')]),('EventResource',[('event','fk:Event'),('name','char'),('status','status')])],
    'finance': [('Budget',[('code','char_unique'),('name','char'),('amount','decimal'),('status','status')]),('Transaction',[('budget','fk:Budget:null'),('reference','char_unique'),('amount','decimal'),('status','status')])],
    'fleet': [('Vehicle',[('code','char_unique'),('name','char'),('status','status')]),('Trip',[('vehicle','fk:Vehicle'),('name','char'),('status','status')]),('Maintenance',[('vehicle','fk:Vehicle'),('name','char'),('status','status')])],
    'health_facilities': [('Hospital',[('code','char_unique'),('name','char'),('status','status')]),('FacilityStatus',[('hospital','fk:Hospital'),('name','char'),('status','status')])],
    'hr': [('Department',[('code','char_unique'),('name','char'),('status','status')]),('JobTitle',[('code','char_unique'),('name','char'),('status','status')]),('Staff',[('person','fk:people.Person'),('department','fk:Department:null'),('job_title','fk:JobTitle:null'),('code','char_unique'),('name','char'),('status','status')])],
    'inventory': [('Warehouse',[('code','char_unique'),('name','char'),('status','status')]),('Stock',[('warehouse','fk:Warehouse'),('sku','char_unique'),('name','char'),('quantity','decimal')]),('Shipment',[('warehouse','fk:Warehouse'),('code','char_unique'),('name','char'),('status','status')]),('Adjustment',[('warehouse','fk:Warehouse'),('code','char_unique'),('name','char'),('status','status')])],
    'locations': [('Location',[('code','char_unique'),('name','char'),('status','status')]),('GeoJsonLayer',[('location','fk:Location:null'),('code','char_unique'),('name','char'),('status','status')]),('MapLayer',[('location','fk:Location:null'),('code','char_unique'),('name','char'),('status','status')])],
    'medical': [('MedicalRecord',[('patient','fk:patients.Patient'),('code','char_unique'),('name','char'),('status','status')]),('Consultation',[('patient','fk:patients.Patient'),('hospital','fk:health_facilities.Hospital:null'),('name','char'),('status','status')])],
    'memberships': [('Member',[('person','fk:people.Person'),('code','char_unique'),('name','char'),('status','status')]),('Subscription',[('member','fk:Member'),('code','char_unique'),('name','char'),('status','status')])],
    'missing_persons': [('MissingPerson',[('code','char_unique'),('name','char'),('status','status')]),('MissingPersonReport',[('missing_person','fk:MissingPerson'),('code','char_unique'),('name','char'),('status','status')])],
    'patients': [('Patient',[('person','fk:people.Person'),('code','char_unique'),('name','char'),('status','status')]),('Referral',[('patient','fk:Patient'),('code','char_unique'),('name','char'),('status','status')])],
    'procurement': [('Vendor',[('code','char_unique'),('name','char'),('status','status')]),('PurchaseRequest',[('code','char_unique'),('name','char'),('status','status')]),('PurchaseOrder',[('vendor','fk:Vendor:null'),('purchase_request','fk:PurchaseRequest:null'),('code','char_unique'),('name','char'),('status','status')])],
    'reporting': [('Report',[('code','char_unique'),('title','char'),('status','status')]),('Dashboard',[('code','char_unique'),('title','char'),('status','status')]),('Metric',[('dashboard','fk:Dashboard'),('code','char_unique'),('name','char'),('amount','decimal')])],
    'requests': [('Request',[('code','char_unique'),('title','char'),('status','status')]),('RequestItem',[('request','fk:Request'),('code','char_unique'),('name','char'),('quantity','decimal')]),('RequestAssignment',[('request','fk:Request'),('assignee','fk:people.Person:null'),('name','char'),('status','status')])],
    'shelters': [('Shelter',[('code','char_unique'),('name','char'),('status','status')]),('Occupancy',[('shelter','fk:Shelter'),('name','char'),('quantity','decimal')]),('Checkin',[('shelter','fk:Shelter'),('name','char'),('status','status')])],
    'victim_identification': [('Victim',[('code','char_unique'),('name','char'),('status','status')]),('Identification',[('victim','fk:Victim'),('code','char_unique'),('name','char'),('status','status')])],
    'volunteers': [('Volunteer',[('person','fk:people.Person'),('code','char_unique'),('name','char'),('status','status')]),('Skill',[('code','char_unique'),('name','char'),('status','status')]),('Availability',[('volunteer','fk:Volunteer'),('name','char'),('status','status')])],
}

ENDPOINTS = {
'org': [('organizations','/api/org/','org.view_organization',['name','code','email','is_active']),('sites','/api/org/sites/','org.view_site',['name','city','address']),('facilities','/api/org/facilities/','org.view_facility',['name','facility_type','status'])],
'people': [('people','/api/people/','people.view_person',['first_name','last_name','gender','date_of_birth']),('contacts','/api/people/contacts/','people.view_contact',['person_name','contact_type','value','is_primary']),('identities','/api/people/identities/','people.view_identity',['person_name','document_type','document_number','issued_country'])],
'projects': [('projects','/api/projects/','projects.view_project',['name','code','status','start_date']),('activities','/api/projects/activities/','projects.view_activity',['project_name','name','status','start_date']),('tasks','/api/projects/tasks/','projects.view_task',['activity_name','title','status','priority'])],
'communications': [('messages','/api/communications/messages/',None,['recipient','channel','subject','status'])],
'hr': [('departments','/api/hr/departments/',None,['code','name','status']),('job-titles','/api/hr/job-titles/',None,['code','name','status']),('staffs','/api/hr/staffs/',None,['code','name','status'])],
'volunteers': [('volunteers','/api/volunteers/volunteers/',None,['code','name','status']),('skills','/api/volunteers/skills/',None,['code','name','status']),('availabilitys','/api/volunteers/availabilitys/',None,['name','status'])],
'requests': [('requests','/api/requests/requests/',None,['code','title','status']),('request-items','/api/requests/request-items/',None,['code','name','quantity']),('request-assignments','/api/requests/request-assignments/',None,['name','status'])],
'inventory': [('warehouses','/api/inventory/warehouses/',None,['code','name','status']),('stocks','/api/inventory/stocks/',None,['sku','name','quantity']),('shipments','/api/inventory/shipments/',None,['code','name','status']),('adjustments','/api/inventory/adjustments/',None,['code','name','status'])],
'assets': [('asset-types','/api/assets/asset-types/',None,['code','name','status']),('assets','/api/assets/assets/',None,['code','name','status']),('assignments','/api/assets/assignments/',None,['assigned_to_name','status'])],
'fleet': [('vehicles','/api/fleet/vehicles/',None,['code','name','status']),('trips','/api/fleet/trips/',None,['name','status']),('maintenances','/api/fleet/maintenances/',None,['name','status'])],
'procurement': [('vendors','/api/procurement/vendors/',None,['code','name','status']),('purchase-requests','/api/procurement/purchase-requests/',None,['code','name','status']),('purchase-orders','/api/procurement/purchase-orders/',None,['code','name','status'])],
'documents': [('documents','/api/documents/documents/',None,['code','title','status']),('file-attachments','/api/documents/file-attachments/',None,['name','status'])],
'reporting': [('reports','/api/reporting/reports/',None,['code','title','status']),('dashboards','/api/reporting/dashboards/',None,['code','title','status']),('metrics','/api/reporting/metrics/',None,['code','name','amount'])],
'finance': [('budgets','/api/finance/budgets/',None,['code','name','amount','status']),('transactions','/api/finance/transactions/',None,['reference','amount','status'])],
'budgets': [('budget-plans','/api/budgets/budget-plans/',None,['code','name','status']),('budget-lines','/api/budgets/budget-lines/',None,['code','name','amount'])],
'memberships': [('members','/api/memberships/members/',None,['code','name','status']),('subscriptions','/api/memberships/subscriptions/',None,['code','name','status'])],
'alerts': [('alerts','/api/alerts/alerts/',None,['code','title','status']),('cap-messages','/api/alerts/cap-messages/',None,['identifier','headline','scope'])],
'shelters': [('shelters','/api/shelters/shelters/',None,['code','name','status']),('occupancys','/api/shelters/occupancys/',None,['name','quantity']),('checkins','/api/shelters/checkins/',None,['name','status'])],
'case_management': [('clients','/api/case-management/clients/',None,['code','name','status']),('case-filess','/api/case-management/case-filess/',None,['case_number','name','status']),('case-events','/api/case-management/case-events/',None,['event_type','status'])],
'health_facilities': [('hospitals','/api/health-facilities/hospitals/',None,['code','name','status']),('facility-statuss','/api/health-facilities/facility-statuss/',None,['name','status'])],
'patients': [('patients','/api/patients/patients/',None,['code','name','status']),('referrals','/api/patients/referrals/',None,['code','name','status'])],
'medical': [('medical-records','/api/medical/medical-records/',None,['code','name','status']),('consultations','/api/medical/consultations/',None,['name','status'])],
'epidemiology': [('epidemiology-cases','/api/epidemiology/epidemiology-cases/',None,['code','name','status']),('contact-traces','/api/epidemiology/contact-traces/',None,['name','status']),('outbreaks','/api/epidemiology/outbreaks/',None,['code','name','status'])],
'events': [('events','/api/events/events/',None,['code','title','status']),('scenarios','/api/events/scenarios/',None,['name','status']),('event-resources','/api/events/event-resources/',None,['name','status'])],
'missing_persons': [('missing-persons','/api/missing-persons/missing-persons/',None,['code','name','status']),('missing-person-reports','/api/missing-persons/missing-person-reports/',None,['code','name','status'])],
'victim_identification': [('victims','/api/victim-identification/victims/',None,['code','name','status']),('identifications','/api/victim-identification/identifications/',None,['code','name','status'])],
'locations': [('locations','/api/locations/locations/',None,['code','name','status']),('geo-json-layers','/api/locations/geo-json-layers/',None,['code','name','status']),('map-layers','/api/locations/map-layers/',None,['code','name','status'])],
'content': [('pages','/api/content/pages/',None,['code','title','status']),('posts','/api/content/posts/',None,['code','title','status']),('news-items','/api/content/news-items/',None,['code','title','status'])],
}

for app, models in APPS.items():
    app_dir = backend/'apps'/app
    app_dir.mkdir(parents=True, exist_ok=True)
    (app_dir/'migrations').mkdir(exist_ok=True)
    (app_dir/'migrations'/'__init__.py').write_text('')
    class_name = ''.join(part.capitalize() for part in app.split('_')) + 'Config'
    (app_dir/'apps.py').write_text(f'from django.apps import AppConfig\n\nclass {class_name}(AppConfig):\n    default_auto_field = "django.db.models.BigAutoField"\n    name = "apps.{app}"\n')
    lines = ['from django.db import models','from apps.core.models import SoftDeleteAuditModel','','']
    for cls, fields in models:
        lines.append(f'class {cls}(SoftDeleteAuditModel):')
        if app not in {'epidemiology','events','victim_identification','missing_persons'}:
            lines.append(f'    organization = models.ForeignKey("org.Organization", on_delete=models.CASCADE, related_name="{cls.lower()}_{app}")')
        for fname, spec in fields:
            if spec.startswith('fk:'):
                target = spec.split(':',1)[1]
                null = False
                if ':null' in target:
                    target = target.replace(':null','')
                    null = True
                on_delete = 'models.SET_NULL' if null else 'models.CASCADE'
                lines.append(f'    {fname} = models.ForeignKey("{target}", on_delete={on_delete}, null={null}, blank={null}, related_name="{cls.lower()}_{fname}")')
            elif spec == 'char_unique':
                lines.append(f'    {fname} = models.CharField(max_length=80, unique=True)')
            elif spec == 'char':
                lines.append(f'    {fname} = models.CharField(max_length=255)')
            elif spec == 'char_blank':
                lines.append(f'    {fname} = models.CharField(max_length=255, blank=True)')
            elif spec == 'status':
                default = 'active' if cls in {'Alert','Event','Shelter','Hospital','Patient','Victim','MissingPerson','Volunteer','Staff'} else 'draft'
                lines.append(f'    {fname} = models.CharField(max_length=50, default="{default}")')
            elif spec == 'decimal':
                lines.append(f'    {fname} = models.DecimalField(max_digits=14, decimal_places=2, default=0)')
            elif spec.startswith('char_default:'):
                d = spec.split(':',1)[1]
                lines.append(f'    {fname} = models.CharField(max_length=100, default="{d}")')
        lines += ['', '    class Meta:', '        ordering = ["-id"]', '', '    def __str__(self):', '        return getattr(self, "title", None) or getattr(self, "name", None) or getattr(self, "code", None) or str(self.pk)', '', '']
    (app_dir/'models.py').write_text('\n'.join(lines).rstrip()+"\n")
    ser = ['from rest_framework import serializers', f'from .models import {", ".join(cls for cls,_ in models)}','','']
    for cls,_ in models:
        ser += [f'class {cls}Serializer(serializers.ModelSerializer):','    class Meta:',f'        model = {cls}','        fields = "__all__"','','']
    (app_dir/'serializers.py').write_text('\n'.join(ser).rstrip()+"\n")
    view = ['from rest_framework import permissions','from apps.core.tenancy import OrganizationScopedQuerySetMixin','from apps.core.viewsets import SoftDeleteAuditModelViewSet',f'from .models import {", ".join(cls for cls,_ in models)}',f'from .serializers import {", ".join(cls+"Serializer" for cls,_ in models)}','','']
    for cls,_ in models:
        inheritance = 'SoftDeleteAuditModelViewSet' if app in {'epidemiology','events','victim_identification','missing_persons'} else 'OrganizationScopedQuerySetMixin, SoftDeleteAuditModelViewSet'
        view += [f'class {cls}ViewSet({inheritance}):',f'    queryset = {cls}.objects.all()',f'    serializer_class = {cls}Serializer','    permission_classes = [permissions.IsAuthenticated]','    search_fields = ["id", "code", "name", "title", "status"]','    ordering_fields = ["id", "created_at", "updated_at"]','','']
    (app_dir/'views.py').write_text('\n'.join(view).rstrip()+"\n")
    url_lines = ['from django.urls import include, path','from rest_framework.routers import DefaultRouter',f'from .views import {", ".join(cls+"ViewSet" for cls,_ in models)}','','router = DefaultRouter()']
    for endpoint, (cls,_) in zip(ENDPOINTS[app], models):
        url_lines.append(f'router.register("{endpoint[0]}", {cls}ViewSet, basename="{endpoint[0]}")')
    url_lines += ['','urlpatterns = [path("", include(router.urls))]']
    (app_dir/'urls.py').write_text('\n'.join(url_lines)+"\n")
    admin_lines = ['from django.contrib import admin', f'from .models import {", ".join(cls for cls,_ in models)}','','']
    for cls,_ in models:
        admin_lines += [f'@admin.register({cls})',f'class {cls}Admin(admin.ModelAdmin):','    list_display = ("id", "created_at", "updated_at")','    search_fields = ("id",)','', '']
    (app_dir/'admin.py').write_text('\n'.join(admin_lines).rstrip()+"\n")

src = frontend/'src'
(src/'config').mkdir(exist_ok=True)
module_configs = []
for section, entries in ENDPOINTS.items():
    for name, endpoint, permission, columns in entries:
        module_configs.append({'key': name.replace('-','_'),'label': name.replace('-',' ').replace('_',' ').title(),'route': name,'endpoint': endpoint.replace('/api',''),'permission': permission,'columns': columns})
(src/'config'/'modules.js').write_text('export const moduleConfigs = '+json.dumps(module_configs, indent=2)+';\n')
(src/'pages'/'ModuleListPage.jsx').write_text(textwrap.dedent('''
import { useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import PageHeader from "../components/crud/PageHeader";
import DataTable from "../components/crud/DataTable";
import DataToolbar from "../components/crud/DataToolbar";
import Pagination from "../components/crud/Pagination";
import EmptyState from "../components/crud/EmptyState";
import usePaginatedList from "../hooks/usePaginatedList";
import { moduleConfigs } from "../config/modules";

export default function ModuleListPage() {
  const { moduleKey } = useParams();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const config = moduleConfigs.find((item) => item.route === moduleKey);
  const { data, isLoading, refetch } = usePaginatedList(config?.key || moduleKey, config?.endpoint || "/", {
    search,
    page,
    ordering: "-created_at",
  });
  const columns = useMemo(() => (config?.columns || []).map((key) => ({
    key,
    label: key.replaceAll("_", " ").replace(/(^|\s)\w/g, (c) => c.toUpperCase()),
    render: (row) => {
      const value = row[key];
      if (typeof value === "boolean") return value ? "Oui" : "Non";
      return value ?? "—";
    },
  })), [config]);

  if (!config) return <EmptyState title="Module introuvable" description="Cette ressource n'est pas configurée." />;
  if (isLoading) return <p>Chargement...</p>;
  const rows = data?.results || data || [];
  return (
    <div>
      <PageHeader title={config.label} description={`Gestion de ${config.label.toLowerCase()}`} />
      <DataToolbar search={search} setSearch={setSearch} onRefresh={refetch} />
      {rows.length ? <DataTable columns={columns} rows={rows} /> : <EmptyState title={`Aucune donnée pour ${config.label.toLowerCase()}`} />}
      <Pagination data={data} onPageChange={(direction) => {
        if (direction === "previous" && page > 1) setPage(page - 1);
        if (direction === "next") setPage(page + 1);
      }} />
    </div>
  );
}
''').strip()+"\n")
(src/'layouts'/'menu.js').write_text(textwrap.dedent('''
import { Box, LayoutDashboard } from "lucide-react";
import { moduleConfigs } from "../config/modules";

export const menuItems = [
  { label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
  ...moduleConfigs.map((item) => ({
    label: item.label,
    to: `/modules/${item.route}`,
    icon: Box,
    permission: item.permission,
  })),
];
''').strip()+"\n")
(src/'App.jsx').write_text(textwrap.dedent('''
import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";
import useBootstrapAuth from "./features/auth/useBootstrapAuth";
import LoginPage from "./features/auth/LoginPage";
import ProtectedRoute from "./routes/ProtectedRoute";
import PermissionRoute from "./routes/PermissionRoute";
import AdminLayout from "./layouts/AdminLayout";
import DashboardPage from "./pages/DashboardPage";
import ModuleListPage from "./pages/ModuleListPage";
import { moduleConfigs } from "./config/modules";

function AppRouter() {
  useBootstrapAuth();
  const router = createBrowserRouter([
    { path: "/login", element: <LoginPage /> },
    {
      path: "/",
      element: <ProtectedRoute><AdminLayout /></ProtectedRoute>,
      children: [
        { index: true, element: <Navigate to="/dashboard" replace /> },
        { path: "dashboard", element: <DashboardPage /> },
        ...moduleConfigs.map((item) => ({
          path: `modules/${item.route}`,
          element: item.permission ? <PermissionRoute permission={item.permission}><ModuleListPage /></PermissionRoute> : <ModuleListPage />,
        })),
      ],
    },
  ]);
  return <RouterProvider router={router} />;
}

export default AppRouter;
''').strip()+"\n")

(base/'README.md').write_text(textwrap.dedent('''
# Relief Platform Django 6 Extended Strict

Base étendue Django 6 + React 19 + Redis, nettoyée pour être plus stricte et plus simple à faire évoluer.

## Inclus

- Backend Django 6, DRF, JWT, RBAC, Celery, Redis, Channels.
- Frontend React + Vite + Tailwind avec tous les modules étendus branchés.
- Docker Compose avec PostgreSQL, Redis, backend, frontend, Celery worker, Celery beat, Flower et Nginx.
- Migrations initiales.
- README de démarrage.

## Démarrage

```bash
docker compose up --build
```

Puis :

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py seed_rbac
```

## URLs utiles

- Frontend: `http://localhost/`
- API: `http://localhost/api/`
- Admin: `http://localhost/admin/`
- Swagger: `http://localhost/api/docs/`
- Flower: `http://localhost:5555/`

## Structure frontend

Le frontend est piloté par `frontend/src/config/modules.js`.
Chaque module étendu est branché automatiquement via `ModuleListPage.jsx` et exposé dans le menu.

## Notes

- Cette version privilégie la cohérence structurelle et la facilité d’extension.
- Les modules étendus fournissent une base CRUD homogène côté backend et côté frontend.
- Les routes étendues sont exposées sous des préfixes API distincts pour éviter les collisions.
''').strip()+"\n")
