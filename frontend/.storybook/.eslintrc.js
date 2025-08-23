module.exports = {
  extends: [
    '../.eslintrc.js',
    'plugin:storybook/recommended',
  ],
  rules: {
    // Regras específicas para Storybook
    'storybook/no-redundant-story-name': 'warn',
    'storybook/await-interactions': 'error',
    'storybook/no-unnecessary-waiting': 'error',
    'storybook/prefer-pascal-case': 'error',
    'storybook/use-storybook-expect': 'error',
    'storybook/use-storybook-testing-library': 'error',
  },
  overrides: [
    {
      files: ['*.stories.@(ts|tsx|js|jsx|mjs|cjs)'],
      rules: {
        // Regras específicas para arquivos de stories
        'import/no-anonymous-default-export': 'off',
        'react-hooks/rules-of-hooks': 'off',
      },
    },
  ],
}
