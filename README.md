# place

`place` is a command line utility that provides functionality similar to `mv`,
but with a small additional feature. First an example of the problem `place` attempts
to solve:

Let's say you are working on a software project and you need to integrate a new tool to that project.
Perhaps you are starting a front end project and need to get `webpack` configured to manage your
assets or you want to create a `docker-compose.yaml` file to containerize your environment. What
ever the tool may be, its possible (and sometimes very likely) that you will run into issues a
spend some non-trivial amount of time tinkering with settings to get things working. A common
issue that I have run into throughout this process is with renaming/moving files. There have
been times where I've moved a file and not updated that files location in the slew of 
configuration files that may point to it. If error messages are not clear, I might not realize
the issue and continue tinkering with settings, not realizing that my configuration is fine
but a file is simply out of place.

That is where `place` comes in! The idea behind `place` is that it will take care of updating
these configuration files for you (via plugins). The canonical example would be a `Makefile`.

Imagine the following simple rule:
```makefile
# in your Makefile
obj/Class.o: src/Class.cpp
    g++ -c src/Class.cpp -o obj/Class.o
```

Now imagine that it is decided that `Class.cpp` is not a very good name. So we can use `place`
to change the name, and the `Makefile` will be updated for us!

```bash
place src/Class.cpp src/BetterName.cpp
```

Now our `Makefile` will look like:
```
# in your Makefile
obj/BetterName.o: src/BetterName.cpp
    g++ -c src/BetterName.cpp -o obj/BetterName.o
```

Now it might look like a lot more than a simple rename occurred in the `Makefile` and that is true.
The key idea with place is that plugins will provide the actual functionality to perform the renaming,
`place` simply acts as the platform and CLI. This allows better control over the tool and allows plugins
to be built by the community.
