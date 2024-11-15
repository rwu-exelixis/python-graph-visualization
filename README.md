# NVL Python Wrapper

This project contains an experimental Python wrapper with the NVL JavaScript library.

## Getting started

To build the Python packages, run

```sh
yarn          # Install JavaScript dependencies
yarn build    # Build JavaScript resources to be used by Python code
pip install . # run with --editable for development mode
```

To test if the wrapper is working and see some examples checkout the `/examples` directory

```sh
jupyter notebook examples/neo4j-nvl-example.ipynb
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

#### JavaScipts configs

* `babel.config.js` - Config for the JavaScript compiler
* `tsconfig.json` - Configuration for TypeScript code
* `package.json` - For yarn, define dependencies and `build` target
* `webpack.config.js` - Config for bundling JS parts

#### Python

Everything is configured inside `pyproject.toml`

To keep a consistent code-style, we use `ruff` and `mypy`.
For convenience there are a couple of scripts:

```sh
./scripts/makestyle.sh # try to fix linting violations and format code
./scripts/checkstyle.sh # check for linting, format or typing issues

```
