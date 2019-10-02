import datetime
import plotly.figure_factory as ff
import argparse

from orgparse import load, loads, node

plan = []
nodeid=''
verbose = False
output = ''
one_day = datetime.timedelta(1)

def set_dates_in_parent_tasks(node_list,plan):
    _start_date = datetime.date.today()
    tasklist = []
    for node in node_list:
        
      if node.get_parent().is_root():
        if nodeid != '':
            if node.get_property("id") is None or node.get_property("id") != nodeid:
                print("GOT HERE")
                continue
        if  node.children:
            task = Task(node.heading)
            task.settype("summary")
            if verbose:
                print(node.heading)
        else:
            # a top-level node with no children isn't part of a project plan
            continue; # Maybe quit here instead?
      else:
          # a child node, so don't duplicate it
          continue 
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
    if verbose:
        print(node.heading)
    #print('-')
    if node.scheduled.start is not None:
      start_date = node.scheduled.start
    else:
      start_date = _start_date
    task = Task(node.heading)
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
      task.settype("summary")
      set_dates_in_child_tasks(node.children,tasklist,task,_start_date=start_date)
    else:
      task.settype("detail")

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

def ganttify(filename, output='gantt.png'):
    root = load(filename)    
    set_dates_in_parent_tasks(root[1:],plan)
    plan.reverse()

    colors = {'summary': 'rgb(0, 0, 0)',
              'detail': 'rgb(50, 70, 238)'}
    fig = ff.create_gantt(plan,colors=colors, index_col='Type')
    #fig.show()
    fig.layout.title="Build the dream home... or the Home build dream"
    fig.layout.yaxis['tickfont'] = {'family': 'Courier New', 'size': 8}
    fig.layout.xaxis['rangeselector']={}
    
    fig.layout.yaxis['showgrid']=True
    fig.layout.xaxis['showgrid']=True

    fig.write_image(output)


'''
if running at the command line, parse the args 
and pass them to ganttify

'''
if __name__ == "__main__":
    
    helptext = "This program tries to create a gantt chart image file from an org-mode file. Usage: -f input org-mode filename -g output image file name"
    #parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description = helptext)
    parser.add_argument('-f', help='The name of the org file to be processed')
    parser.add_argument('-g', help='The name of the gantt chart image file to produce', default="gantt.png")
    parser.add_argument('-id', help='the id of the root node to be processed, if the org file contains additional nodes other than the project plan.')
    parser.add_argument('-v', action='store_true', help='print each node as it is processed.')
    args = parser.parse_args()
    filename = args.f
    verbose = args.v
    output = args.g
    
    print('-f',args.f)
    print('-id',args.id)
    print('-v',args.v)
    ganttify(filename,output)
