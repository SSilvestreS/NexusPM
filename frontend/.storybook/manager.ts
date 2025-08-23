import { addons } from '@storybook/manager-api'
import { themes } from '@storybook/theming'

// Configuração do manager do Storybook
addons.setConfig({
  theme: {
    ...themes.dark,
    brandTitle: 'Nova Pasta',
    brandUrl: 'https://nova-pasta.com',
    brandImage: '/logo.png',
  },
  selectedPanel: 'controls',
  initialActive: 'sidebar',
  showNav: true,
  showPanel: true,
  panelPosition: 'bottom',
  enableShortcuts: true,
  showToolbar: true,
  selectedTool: 'zoom',
  sidebar: {
    showRoots: true,
    collapsedRoots: ['other'],
  },
  // Configurações de viewport
  viewport: {
    viewports: {
      mobile: {
        name: 'Mobile',
        styles: {
          width: '375px',
          height: '667px',
        },
      },
      tablet: {
        name: 'Tablet',
        styles: {
          width: '768px',
          height: '1024px',
        },
      },
      desktop: {
        name: 'Desktop',
        styles: {
          width: '1280px',
          height: '720px',
        },
      },
    },
  },
  // Configurações de backgrounds
  backgrounds: {
    default: 'light',
    values: [
      {
        name: 'light',
        value: '#ffffff',
      },
      {
        name: 'dark',
        value: '#1f2937',
      },
      {
        name: 'primary',
        value: '#3b82f6',
      },
    ],
  },
})
