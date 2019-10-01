# orgpygantt
A Python library for converting org-mode node trees to gantt charts.

## About
[Org-mode](https://www.orgmode.org/) is an emacs major mode for managing to-do lists, calendars, taks, projects, and more. A typical use case would involve a project file containing a hierarchical set of nodes and subnodes, each representing a task or subtask.

Org-mode also supports due dates and deadlines, effort estimates, and status (pending, complete, etc.

All of these can be used to define a series of parent tasks and subtasks that could be displayed in a [gantt chart](https://en.wikipedia.org/wiki/Gantt_chart). 

Orgpygantt assumes a series of org-mode nodes representing parent or child task. The very first top-level task includes a start date (Today's date will be used if no start date is specified), and each non-parent task has an estimated effort value (the default value of 1 day will be used if no effort is specified).

## Dependencies
It depends on the following libraries:
* To convert an org-mode node tree into Python,
https://github.com/karlicoss/orgparse
* Then this library turns that into a list of tasks, each with a specific (though perhaps speculative) start and end date.
* Plotly is used produce the gantt chart. Plotly, in turn, depends on:
  * Orca: https://github.com/plotly/orca/releases
  * Fuse: $ sudo apt-get install fuse