class Interval:
  def __init__(self, start, end):
    self.start = start
    self.end = end

  def __repr__(self):
    return f"[{self.start}, {self.end}]"

  def print_interval(self):
    print("[" + str(self.start) + ", " + str(self.end) + "]", end='')

def convert_to_intervals(intervals):
    interval_objects = []
    for i in intervals:
        interval_objects.append(Interval(i[0], i[1]))
    return interval_objects