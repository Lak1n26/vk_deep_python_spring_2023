#! /usr/bin/env python3

from setuptools import setup, Extension


def main():
    setup(name="cjson",
          version = "1.1.0",
          author="Danila Lyapin",
          ext_modules=[
              Extension('cjson', ['cjson.c'])
          ]
          )


if __name__ == "__main__":
    main()