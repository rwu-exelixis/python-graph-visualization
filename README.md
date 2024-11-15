# NVL Python Wrapper

This project contains an experimental Python wrapper with the NVL JavaScript library.

## Getting started

To build the Python packages, run

```
yarn
yarn build
yarn install-package # or `pip install .`
```

To test if the wrapper is working and see some examples, you can use the `neo4j-nvl-example.ipynb` notebook:

```
jupyter notebook neo4j-nvl-example.ipynb
```


## Development

### Project structure

This is a multi-language project.

```
/src
    /neo4j_viz #python code to produce HTML(+JS) file
    /nvl_entrypoint # defines JavaScript code + packages it to be used by neo4j-viz
/tests
```

`babel.config.js` - Config for the JavaScript compiler
`tsconfig.json` - Configuration for TypeScript code
`package.json` - ...
`webpack.config.js` -
