module.exports = {
  docsSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Architecture',
      items: ['architecture/core-stack', 'architecture/genui-stack'],
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
      ],
    },
    {
      type: 'category',
      label: 'Runbooks',
      items: ['runbooks/memory-eviction'],
    },
  ],
};
