module.exports = {
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Architecture',
      items: [
        'architecture/core-stack',
        'architecture/genui-stack',
        'architecture/secure-agents',
      ],
    },
    {
      type: 'category',
      label: 'AIOps and MCP',
      items: ['aiops-mcp/grafana-mcp', 'aiops-mcp/prometheus-mcp'],
    },
    {
      type: 'category',
      label: 'Deployment',
      items: [
        'deployment/host-prereqs',
        'deployment/configuration-env',
        'deployment/dashboards',
        'deployment/telemetry-contract',
        'deployment/exporters-security-tools',
      ],
    },
    {
      type: 'category',
      label: 'Runbooks',
      items: ['runbooks/memory-eviction'],
    },
    {
      type: 'category',
      label: 'Security',
      items: ['security/owasp-agent-controls'],
    },
  ],
};
