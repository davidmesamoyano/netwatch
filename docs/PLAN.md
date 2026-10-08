# Plan de trabajo de NetWatch (3 semanas)

Marca cada casilla al terminarla. Regla de oro: no pases a la siguiente tarea sin entender lo que has hecho.

## Semana 1 – La app y Docker

- [ ] Día 1: leer y entender `probe/netwatch/` (stats, measure, config, metrics, main). Ejecutar los tests (`pytest`).
- [ ] Día 2: arrancar todo con Docker Compose y ver las métricas en Prometheus. Probar `sites/degrade.sh`.
- [ ] Día 3: añadir un endpoint `/healthz` a la sonda (lo usará Kubernetes para saber si está viva).
- [ ] Día 4: mejorar el Dockerfile a multi-stage y comprobar el tamaño de la imagen (`docker images`).
- [ ] Día 5: crear el repo público en GitHub, primer commit y README con una captura de Prometheus.

## Semana 2 – Infraestructura, Kubernetes y Jenkins

- [ ] Día 1: `infra/ansible/` – playbook que instala Docker, kind, kubectl, Helm y Terraform (idempotente).
- [ ] Día 2: `infra/terraform/` – crea el clúster kind e instala kube-prometheus-stack y Jenkins con el provider de Helm.
- [ ] Días 3-4: `charts/netwatch/` – Helm chart con la sonda (Deployment, Service, ConfigMap, ServiceMonitor) y las sedes.
- [ ] Día 5: `jenkins/` – Jenkins configurado como código (JCasC) y primer Jenkinsfile que hace `helm upgrade`.

## Semana 3 – Pipelines, observabilidad y presentación

- [ ] Día 1: `.github/workflows/ci.yml` – lint, tests, build, Trivy, push a GHCR y prueba E2E con kind.
- [ ] Día 2: Jenkinsfile completo (terraform plan, ansible-lint, helm upgrade, smoke test, rollback) + panel de Jenkins en Grafana.
- [ ] Día 3: paneles de Grafana como código (red y SLO), reglas de alerta y avisos por Telegram.
- [ ] Día 4: script de caos y vídeo de 2 minutos de la demo completa.
- [ ] Día 5: README final con diagrama, decisiones técnicas y problemas resueltos. Post en LinkedIn.
