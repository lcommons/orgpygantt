# orgpygantt
A Python library for converting org-mode node trees to gantt charts.

This first pass work, but just barely. It assumes a series of org-mode nodes representing parent or child task. The very first top-level task includes a start date, and each non-parent task has an estimated effort value.
It depends on the following libraries:
* To convert an org-mode node tree into Python,
https://github.com/karlicoss/orgparse
* Then this library turns that into a list of tasks, each with a specific (though perhaps speculative) start and end date.
* Plotly is used produce the gantt chart. Plotly, in turn, depends on:
  * Orca: https://github.com/plotly/orca/releases
  * Fuse: $ sudo apt-get install fuse