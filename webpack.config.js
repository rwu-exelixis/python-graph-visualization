const path = require('path')

module.exports = [
  {
    name: 'base',
    mode: 'production',
    entry: {
      base: ['./src/nvl_entrypoint/index.ts']
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules|dist/,
          use: 'babel-loader'
        },
        {
          test: /\.ts$/,
          use: 'ts-loader',
          exclude: /node_modules/
        }
      ]
    },
    resolve: {
      extensions: ['.ts', '.js']
    },
    output: {
      path: path.resolve(__dirname, 'src/neo4j_viz/resources/nvl_entrypoint'),
      publicPath: '',
      library: 'NVLBase',
      libraryTarget: 'var',
      clean: true
    }
  }
]
