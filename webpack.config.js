const path = require('path')

module.exports = [
  {
    name: 'base',
    mode: 'production',
    entry: {
      base: ['./src/index.ts']
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
      path: path.resolve(__dirname, 'nvl_package/dist'),
      publicPath: '',
      library: 'NVLBase',
      libraryTarget: 'var',
      clean: true
    }
  }
]
