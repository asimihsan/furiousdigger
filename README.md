# furiousdigger

Recommend news articles based on user feedback

## Design

furiousdigger is composed of two parts:

-   A thin Django backend that stores and serves data over a RESTful
    HTTP API. The intention is to avoid using the Django backend for
    most views.
-   A thin angularjs frontend that consumes data over a RESTful
    HTTP AIP. It is independent of this particular Django backend but
    in practice the two will be used together.

## Installation

TODO