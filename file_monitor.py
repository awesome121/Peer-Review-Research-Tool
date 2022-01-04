""""
File monitor: Keep watching files' changes


"""

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler



class FileMonitor:
    def __init__(self, target_file):
        self.target_patterens = [target_file]
        ignore_patterns, ignore_directories, case_sensitive = None, True, True
        self.event_handler = PatternMatchingEventHandler(self.target_patterens, ignore_patterns, ignore_directories, case_sensitive)
        self.event_handler_binding()
        self.observer = Observer()
        path, go_recursively = ".", False
        self.observer.schedule(self.event_handler, path, recursive=go_recursively)
    
    def event_handler_binding(self):
        self.event_handler.on_modified = on_modified
        # self.event_handler.on_moved = on_moved
        # self.event_handler.on_created = on_created
        # self.event_handler.on_deleted = on_deleted

def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")

# def on_created(event):
#     print(f"hey, {event.src_path} has been created!")

# def on_deleted(event):
#     print(f"what the f**k! Someone deleted {event.src_path}!")

# def on_moved(event):
#     print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")