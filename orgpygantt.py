import datetime
import plotly.figure_factory as ff

from orgparse import load, loads, node

plan = []

#orgfile = '/home/lcommons/whereisthis/lcommons/org-files/house2.org'
#root = load('/home/lcommons/whereisthis/lcommons/org-files/house2.org')
orgtree='''#+TITLE: The Plan for Building Our House
#+HTML_HEAD: <link rel="stylesheet" type="text/css" href="style/style1.css" />
#+HTML_HEAD_EXTRA: <link rel="alternate stylesheet" type="text/css" href="style2.css" />

* House build plan
  SCHEDULED: <2020-09-16 Wed>
  :PROPERTIES:
  :ID:       house-plan
  :ORDERED:  t
  :END:      
** Site prep
  :PROPERTIES:
  :END:      
*** Level house site
    :PROPERTIES:
    :Effort:   16:00
    :END:      
*** drainage
    :PROPERTIES:
    :Effort:   16:00
    :END:      
*** septic system
    :PROPERTIES:
    :Effort:   16:00
    :END:      
*** Excavate for foundation 
    :PROPERTIES:
    :Effort:   40:00
    :END:      
** Foundation
  :PROPERTIES:
  :END:      
*** Waste Water drain pipe install     
   :PROPERTIES:
   :Effort:   48:00
   :END:
**** Layout exact location of each drain
   :PROPERTIES:
   :Effort:   8:00
   :END:
**** trench for waste water drains
   :PROPERTIES:
   :Effort:   8:00
   :END:
**** gravel in waste water drain trenchs
   :PROPERTIES:
   :Effort:   8:00
   :END:
**** install waste water drains
   :PROPERTIES:
   :Effort:   16:00
   :END:
   :END:
*** add additional gravel 
   More information about the [[file:slab.org][how the slab is built]].
   :PROPERTIES:
   :Effort:   8:00
   :END:
*** Add insulation 
   More information about the [[file:slab.org][how the slab is built]].
   :PROPERTIES:
   :Effort:   8:00
   :END:
*** rebar, wire mesh
   :PROPERTIES:
   :Effort:   24:00
   :END:
*** Radiant Heat
Read more about the [[file:radiant-heat.org][radiant heat plan]]
   :PROPERTIES:
   :Effort:   16:00
   :END:
*** Build Forms
   More information about how the forms will be built [[file:slab.org][here]].
   :PROPERTIES:
   :Effort:   40:00
   :END:
*** pour slab
   :PROPERTIES:
   :Effort:   8:00
   :END:
** Cut timbers
   :PROPERTIES:
   :Effort:   160:00
   :END:
** Assemble bents 
   :PROPERTIES:
   :Effort:   40:00
   :END:
** Raise Frame
   :PROPERTIES:
   :Effort:   40:00
   :END:
** Roof
   More information about the [[file:roof.org][roof]].
   :PROPERTIES:
   :Effort:   80:00
   :END:      
** Walls
   More information about the plan for the [[file:walls.org][walls]].
   :PROPERTIES:
   :Effort:   160:00
   :END:
** Interior
*** Utility room
   More information about the plan for the [[file:utilityroom.org][utility room]].
   :PROPERTIES:
   :Effort:   80:00
   :END:
*** Laundry room
   :PROPERTIES:
   :Effort:   40:00
   :END:
*** Mud room
   More information about the plan for the [[file:mudroom.org][mud room]].
   :PROPERTIES:
   :Effort:   24:00
   :END:
*** Kitchen
   More information about the plan for the [[file:kitchen.org][kitchen]].
   :PROPERTIES:
   :Effort:   120:00
   :END:
*** bathrooms
   More information about the plan for the [[file:bathrooms.org][bathrooms]].
   :PROPERTIES:
   :Effort:   40:00
   :END:
*** living room
   More information about the plan for the [[file:livingroom.org][living room]].
   :PROPERTIES:
   :Effort:   40:00
   :END:
*** master bedroom
   More information about the plan for the [[file:masterbedroom.org][master bedroom]].
   :PROPERTIES:
   :Effort:   40:00
   :END:
*** other bedrooms
   More information about the plan for the [[file:bedrooms.org][bedrooms]].
   :PROPERTIES:
   :Effort:   40:00
   :END:
** move in!  :milestone:
    :PROPERTIES:
    :ID: movein
    :END:
'''



one_day = datetime.timedelta(1)

def set_dates_in_parent_tasks(node_list,plan):
    _start_date = datetime.date.today()
    tasklist = []
    for node in node_list:
      if node.get_parent().is_root():
        task = Task(node.heading)
        task.settype("summary")
      if node.scheduled.start is not None:
          start_date = node.scheduled.start
      else:
          start_date = _start_date
          task.setstart(start_date)
      if node.get_property("End_date") is None: # set default to one day
        if node.get_property("Effort") is None:
            effort = 1 # Days
        else:
            effort = int(node.get_property("Effort")) / (8*60) # minutes --> days
            newe = task.start + datetime.timedelta(days=effort)
            task.setend(newe)
      else:
          task.setend(node.get_property("End_date"))
          tasklist.append(task)
      if node.children:
          set_dates_in_child_tasks(node.children,tasklist,task,_start_date=start_date)

      _start_date = task.end + one_day

    for task in tasklist:
      plan.append(task.todict())

# Given a node list and a start date, set and calculate the start and end dates
# of the child nodes of this_node
def set_dates_in_child_tasks(this_node_list,tasklist,parent_task, _start_date= None):
  for node in this_node_list:
    if node.scheduled.start is not None:
      start_date = node.scheduled.start
    else:
      start_date = _start_date
    task = Task(node.heading)
    task.settype("detail")
    task.setstart(start_date)
    if node.get_property("End_date") is None: # set default to one day
      if node.get_property("Effort") is None:
        effort = 1 # Days
      else:
        effort = int(node.get_property("Effort")) / (8*60) # minutes --> days
      newe = task.start + datetime.timedelta(days=effort)
      task.setend(newe)
      parent_task.setend(newe)
    else:
      task.setend(node.get_property("End_date"))
    tasklist.append(task)
    if node.children:
      set_dates_in_child_tasks(node.children,tasklist,task,_start_date=start_date)
    
    _start_date = task.end + one_day

class Task:
  def __init__(self, description, start= None, end= None):
    self.description = description
    self.start = start
    if isinstance(end,datetime.date):
      self.end = datetime.datetime.combine(end, datetime.datetime.min.time())
    if isinstance(end,datetime.datetime):
      self.end = end
    elif isinstance(end,int):
      self.end = datetime.datetime(end)
    elif isinstance(end,str):
      self.end = datetime.datetime( int(end) )
    else:
      self.end = end
    self.tasktype = ''

  def setstart(self,start):
    self.start = start
  
  def setend(self,end):
    if isinstance(end,datetime.date):
      self.end = datetime.datetime.combine(end, datetime.datetime.min.time())
    elif isinstance(end,datetime.datetime):
      self.end = end
    elif isinstance(end,int):
      self.end = datetime.datetime(end)
    elif isinstance(end,str):
      self.end = datetime.datetime( int(end) )
    else:
      self.end = None
    
  def settype(self, type):
    self.tasktype = type

  def todict(self):
    dict = {}
    dict["Task"] = self.description
    dict["Start"] = self.start
    if isinstance(self.end,datetime.datetime):
      dict["Finish"] = self.end.replace(hour=23,minute=59)
    dict["Type"] = self.tasktype

    return dict
    
root = loads(orgtree)
set_dates_in_parent_tasks(root[1:],plan)

plan.reverse()
colors = {'summary': 'rgb(0, 0, 0)',
          'detail': 'rgb(50, 70, 138)'}
fig = ff.create_gantt(plan,colors=colors, index_col='Type')
#fig.show()
fig.write_image("fig1.png")
