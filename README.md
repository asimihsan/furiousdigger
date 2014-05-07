# furiousdigger

Recommend news articles based on user feedback

## Requirements

-   Requires a clone and full build of (https://github.com/asimihsan/handytrowel)[https://github.com/asimihsan/handytrowel]
    at the same directory level as the clone of furiousdigger. e.g.
    if you have `/opt/furiousdigger/` you'd also need
    `/opt/handytrowel`.
-   Working CPython 2.x or CPython 3.x installation.

## Design

furiousdigger is composed of two parts:

-   A thin Django backend that stores and serves data over a RESTful
    HTTP API. The intention is to avoid using the Django backend for
    most views.
-   A thin angularjs frontend that consumes data over a RESTful
    HTTP API. It is independent of this particular Django backend but
    in practice the two will be used together.

## Installation

TODO