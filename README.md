# orgpygantt
A Python library for converting org-mode node trees to gantt charts.

## About
[Org-mode](https://www.orgmode.org/) is an emacs major mode for managing to-do lists, calendars, tasks, projects, and more. A typical use case might involve a project file containing a hierarchical set of nodes and subnodes, each representing a task or subtask.

Org-mode also supports due dates and deadlines, effort estimates, and status (pending, complete, etc.)

All of these can be used to define a series of parent tasks and subtasks that could be displayed in a [gantt chart](https://en.wikipedia.org/wiki/Gantt_chart) using Orgpygantt.

Orgpygantt assumes a series of org-mode nodes representing parent or child task. The very first top-level task includes a start date (Today's date will be used if no start date is specified), and each non-parent task has an estimated effort value (the default value of 1 day will be used if no effort is specified). Orgpygantt uses the start date and the duration estimates to calculate start and end dates for each task.

## Limitations
Orgpygantt (currently) works in just one direction: from a start date to and end date. It is entirely possible to build a project plan in the opposite direction, starting from a deadline or planned finish date and work backwards. I just haven't implemented that yet because that isn't my immediate use case.

## Dependencies
Orgpygantt depends on the following libraries:
* To convert an org-mode node tree into Python objects,
https://github.com/karlicoss/orgparse
* [Plotly](https://plot.ly/) is used produce the gantt chart. Plotly, in turn, depends on:
  * Orca: https://github.com/plotly/orca/releases
  * Fuse: $ sudo apt-get install fuse
