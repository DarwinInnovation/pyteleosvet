# pyteleosvet

Python module to simplify accessing data from the [Teleos Veterinary Practice Management System](http://www.teleosvet.com/).

This package provides helper functions and classes that make querying the Teleos mysql database easier. It is built on
the [peewee](http://docs.peewee-orm.com/en/latest/) Python ORM library, which greatly simplifies building complex queries.

## Notes

**This software is provided completely without guarantee or warranty, and no responsibility is taken for its use.**

It is recommended that if you do want to use the library, you set-up new database users with *limited access*. Ideally,
if you are just writing queries you should use a *read-only* user.

So far, this module hss only be tried on Python 3.

## Installation

The package is available using pip:

```
pip install pyteleosvet
```

Then you will need to create a `teleos.json` file with your database details in. A template file is provided.

## Sample scripts

A couple of sample scripts are supplied which demonstrate the package's use.

## Documentation

To follow - but please feel free to post queries via GitHub issues.
