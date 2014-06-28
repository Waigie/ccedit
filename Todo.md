####Refactoring

* rename "choices" to dimes - __Done__
* separate configuration and pretty printing - __Done__
* equivalence (structural and semantic) - __Done__
* equiv should not use prettyprinting - __Done__

####Testing

* add tests to check increase/decrease dimension arity - __Done__
* more equivalence tests
* testing dims and configs method

####Near Furture:
* GUI
    * add .dims file to store project dimensions and alternative names (dims file in the same directory as the source, 
    one dims file per dir)
    * dims file only editable via sidebar
    * dims in source but not in dims files => error
    * only work in view mode
    * update source on save or user action
    