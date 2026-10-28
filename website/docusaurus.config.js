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

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

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
            href: 'https://github.com/waitesgithub/dockprom-ai',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        copyright: `Copyright © ${new Date().getFullYear()} Dockprom-AI. Built with Docusaurus v3.10.2.`,
      },
      colorMode: {
        defaultMode: 'dark',
        respectPrefersColorScheme: true,
      },
    }),
};

module.exports = config;
