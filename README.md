[![Build Status](https://travis-ci.org/AartGoossens/wattbikehublib.svg?branch=master)](https://travis-ci.org/AartGoossens/wattbikehublib)
# wattbikehublib
Python library that provides access to Wattbike sessions and other data stored in the Wattbike Hub.

## Features
- List activities
- Get data from single sessions
- Get training zones
- Get current zone record
- Get historical zone records
- Get username from Wattbike Hub homepage

## How does it work?
The Wattbike Hub does not offer a public API. Well... to be more accurate: the API is not documented. There are a few API endpoints that are used by both the website and apps that offer some API functionality. I used these endpoints to build this library.

## Requirements
- Python 3 (Parts of the code might work in Python 2. Full support for Python 2 is not planned)
- All the libraries in requirements.txt installed (in your virtualenv).
- Wattbike Hub account set to 'publicly viewable'. Check this in your [Wattbike Hub settings](http://hub.wattbike.com/account/edit)

## License
The code in this repository is licensed under the [MIT License](http://choosealicense.com/licenses/mit/). GitHub [describes](http://choosealicense.com) this license as follows:
> The MIT License is a permissive license that is short and to the point. It lets people do anything they want with your code as long as they provide attribution back to you and don’t hold you liable.
My summary: Use this code for whatever you want, but give me credit every single time.
