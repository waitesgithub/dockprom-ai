// @ts-check
/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Dockprom-AI',
  tagline: 'Production-Grade AI Observability & AIOps Platform',
  favicon: 'img/dockprom-ai-logo.png',

  url: 'https://waitesgithub.github.io',
  baseUrl: '/dockprom-ai/',
  organizationName: 'waitesgithub',
  projectName: 'dockprom-ai',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Dockprom-AI',
        logo: {
          alt: 'Dockprom-AI Logo',
          src: 'img/dockprom-ai-logo.png',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docsSidebar',
            position: 'left',
            label: 'Documentation',
          },
          {
            to: '/architecture/core-stack',
            label: 'Architecture',
            position: 'left',
          },
          {
            to: '/deployment/host-prereqs',
            label: 'Deploy',
            position: 'left',
          },
          {
            href: 'https://github.com/waitesgithub/dockprom-ai',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Learn',
            items: [
              {label: 'Overview', to: '/'},
              {label: 'Core architecture', to: '/architecture/core-stack'},
              {label: 'GenUI architecture', to: '/architecture/genui-stack'},
            ],
          },
          {
            title: 'Operate',
            items: [
              {label: 'Configuration', to: '/deployment/configuration-env'},
              {label: 'Dashboards', to: '/deployment/dashboards'},
              {label: 'Runbooks', to: '/runbooks/memory-eviction'},
            ],
          },
          {
            title: 'Project',
            items: [
              {label: 'GitHub', href: 'https://github.com/waitesgithub/dockprom-ai'},
              {label: 'Grafana MCP', to: '/aiops-mcp/grafana-mcp'},
              {label: 'Prometheus MCP', to: '/aiops-mcp/prometheus-mcp'},
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Dockprom-AI. Built with Docusaurus v3.10.2.`,
      },
      announcementBar: {
        id: 'genui_companion',
        content: 'New: Generative UI companion stack with Ollama and pgvector runbook retrieval.',
        backgroundColor: '#0b1120',
        textColor: '#cbd5e1',
        isCloseable: true,
      },
      colorMode: {
        defaultMode: 'dark',
        respectPrefersColorScheme: true,
      },
    }),
};

module.exports = config;
