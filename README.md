# place

`place` is a command line utility that provides functionality similar to `mv`,
but with a small additional feature. It will use plugins to detect references to
the moved file in common development configuration files (`Makefile`, `webpack.config.json`, `package.json`, etc) and update those as well.
