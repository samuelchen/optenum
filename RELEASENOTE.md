
# v1.1.8

* Do not convert Option.text to string. It may cause `gettext_lazy` executed so that some times error occurs in Django.

# v1.1.7

* (lost information)

# v1.1.6

* Group supports +(plus) operator

# v1.1.5

* Fix issue of creating single option group as class attribute

# v1.1.4

* Fix option not found issue when creating option group as class attribute (class attributes creation is not in order)
* Fix option attributes order in python 3.4 & 3.5

# v1.1.3

* Tagged option group support construct as class attribute and support +, -
* fix "random ordered options in group" issue
* fix "tag name checking" issue

# v1.1.2

* Support Option tags 
* Support access tagged options as group (tuple)
* fix "Option.get_text is missed" issue.

# v1.1.1

* Fix issue that `__IGNORE_INVALID_NAME__` does not work.

# v1.1.0

* Change `Option` to make its instance object same as its `code`. 

# v1.0.0

* General Available