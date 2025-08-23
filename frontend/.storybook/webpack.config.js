const path = require('path')

module.exports = ({ config }) => {
  // Resolver de alias para importações
  config.resolve.alias = {
    ...config.resolve.alias,
    '@': path.resolve(__dirname, '../src'),
  }

  // Configuração para arquivos CSS
  config.module.rules.push({
    test: /\.css$/,
    use: ['style-loader', 'css-loader', 'postcss-loader'],
    include: path.resolve(__dirname, '../'),
  })

  // Configuração para arquivos de imagem
  config.module.rules.push({
    test: /\.(png|jpe?g|gif|svg)$/i,
    type: 'asset/resource',
  })

  // Configuração para arquivos de fonte
  config.module.rules.push({
    test: /\.(woff|woff2|eot|ttf|otf)$/i,
    type: 'asset/resource',
  })

  return config
}
