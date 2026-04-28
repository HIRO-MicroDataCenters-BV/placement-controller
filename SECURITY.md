# Security

Security principles and gatekeeping for the placement-controller.

## Security Principles

1. **Zero Trust**: All external services authenticated
2. **least Privilege**: Agents have minimal permissions
3. **Secrets Management**: All secrets in secure storage
4. **Audit Trail**: All actions logged

## Authentication

### Kubernetes API

- Service account tokens
- RBAC for least privilege
- mTLS for service-to-service

### Placement API

- API keys for zone communication
- Token rotation every 24 hours
- Mutual TLS for cross-zone calls

## Authorization

### Agent Permissions

```yaml
# Agent RBAC
rules:
  - apiGroups: [""]
    resources: ["pods", "nodes"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["dcp.hiro.io"]
    resources: ["*"]
    verbs: ["get", "list", "watch", "patch"]
```

### Cross-Zone Access

- Zone-specific tokens
- Limited to required resources
- No cross-zone impersonation

## Secrets Management

### Storage

- Kubernetes Secrets
- Encrypted at rest
- Rotation managed by operators

### Usage

```python
# Never log secrets
# Mask in all output
# Inject via environment
```

## Audit Logging

### Required Events

- [ ] Action execution
- [ ] State transitions
- [ ] API calls
- [ ] Configuration changes

### Log Format

```json
{
  "timestamp": "ISO8601",
  "action_type": "GetType",
  "application": "ns/name",
  "zone": "zone1",
  "success": true
}
```

## Compliance

### CI/CD Security

- Scans for secrets in code
- Vulnerability checking
- SBOM generation

### Runtime Security

- Non-root containers
- Read-only filesystem
- Network policies

---

*Auto-generated from security requirements*
