import type { Preview } from '@storybook/react'
import '../src/index.css'

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    viewport: {
      viewports: {
        mobile: { name: 'Mobile', styles: { width: '375px', height: '667px' } },
        tablet: { name: 'Tablet', styles: { width: '768px', height: '1024px' } },
        desktop: { name: 'Desktop', styles: { width: '1280px', height: '720px' } },
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1f2937' },
        { name: 'primary', value: '#3b82f6' },
      ],
    },
    layout: 'centered',
    docs: {
      toc: true,
      source: { state: 'open' },
    },
  },
  decorators: [
    (Story) => (
      <div style={{ margin: '1em', fontFamily: 'Inter, system-ui, sans-serif' }}>
        <Story />
      </div>
    ),
  ],
}

export default preview
