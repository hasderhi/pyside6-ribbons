# PySide6 Ribbon Menu

## Intro

A minimal, easy-to-read example showing how to implement a custom ribbon-style menu in PySide6 without external UI libraries.
This project is a reference implementation of the DIY ribbon UI used in several of my apps, after some people asked me how it was built.

## Features

- **Custom Ribbon Menu**: Built entirely with PySide6 widgets (QTabBar, QStackedWidget, QToolButton, custom grouping).

- **Ribbon Groups**: Reusable RibbonGroup widget with automatic button grid layout.

- **MIT-Licensed**: Free to use in your own apps, modify, and redistribute (Just credit my work).

## Test it

0. Make sure you have Python 3.X installed
1. Install the requirements
2. Run `main.py`

## Include in your own app

1. Make sure the dependencies are in your requirements
2. Add the classes `RibbonGroup` and `RibbonMenu` to your codebase
3. Replace all `example` and `about` sections with your own menu entries
4. In the constructor of your `MainWindow` class, assign each entry a function

    ```python
    example_ops = {
        "about": self.about,
        "greet": self.greet
    }
    ```

5. Create the menu like this:

    ```python
    self.ribbon = RibbonMenu(example_ops)
    self.setMenuWidget(self.ribbon)
    ```

6. That's it! Please be nice and credit my work :)

## Author & Licensing

### Annabeth Kisling

[annabeth@tk-dev-software.com](mailto:annabeth@tk-dev-software.com)

[tk-dev-software.com](https://tk-dev-software.com)

### Licensing

See `license.md`
