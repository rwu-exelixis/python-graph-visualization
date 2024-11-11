const path = require('path')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const GenerateJsonWebpackPlugin = require('generate-json-webpack-plugin')
const basePackageJson = require('./package.json')

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
    plugins: [
      new GenerateJsonWebpackPlugin(
        'package.json',
        {
          name: basePackageJson.name,
          main: './base.js',
          version: basePackageJson.version,
          license: basePackageJson.license
        },
        null,
        2
      )
    ],
    output: {
      path: path.resolve(__dirname, 'nvl_package/dist'),
      publicPath: '',
      library: 'NVLBase',
      libraryTarget: 'var',
      clean: true
    }
  }
]
