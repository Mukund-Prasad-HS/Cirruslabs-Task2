import streamlit as st
from collections import deque

class TaskQueue:
    def __init__(self):
        self.queue = deque()
        self.completed_tasks = []

    def add_task(self, task):
        self.queue.append(task)

    def add_multiple_tasks(self, tasks):
        self.queue.extend(tasks)

    def complete_task(self):
        if not self.is_empty():
            task = self.queue.popleft()
            self.completed_tasks.append(task)
            return task
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        return None

def main():
    st.title("Task Queue Manager")

    if 'task_queue' not in st.session_state:
        st.session_state.task_queue = TaskQueue()

    st.subheader("Add Tasks")
    new_task = st.text_input("Enter a new task:")
    if st.button("Add Single Task"):
        if new_task:
            st.session_state.task_queue.add_task(new_task)
            st.success(f"Task '{new_task}' added to the queue!")
            st.experimental_rerun()
        else:
            st.warning("Please enter a task before adding.")

    multiple_tasks = st.text_area("Enter multiple tasks (one per line):")
    if st.button("Add Multiple Tasks"):
        tasks = [task.strip() for task in multiple_tasks.split('\n') if task.strip()]
        if tasks:
            st.session_state.task_queue.add_multiple_tasks(tasks)
            st.success(f"{len(tasks)} tasks added to the queue!")
            st.rerun()
        else:
            st.warning("Please enter at least one task.")

    st.subheader("Current Queue Status")
    queue_size = st.session_state.task_queue.size()
    st.write(f"Tasks in queue: {queue_size}")
    if queue_size > 0:
        st.write(f"Next task to be processed: {st.session_state.task_queue.peek()}")
    else:
        st.write("No tasks in the queue at the moment.")

    if st.button("Process Next Task"):
        if not st.session_state.task_queue.is_empty():
            completed_task = st.session_state.task_queue.complete_task()
            st.success(f"Completed task: {completed_task}")
            st.rerun()
        else:
            st.warning("No tasks in the queue!")

    st.subheader("All Tasks in Queue")
    if queue_size > 0:
        for i, task in enumerate(st.session_state.task_queue.queue, 1):
            st.text(f"{i}. {task}")
    else:
        st.write("No tasks in the queue at the moment.")

    st.subheader("Completed Tasks")
    if st.session_state.task_queue.completed_tasks:
        for i, task in enumerate(st.session_state.task_queue.completed_tasks, 1):
            st.text(f"{i}. {task}")
    else:
        st.write("No tasks have been completed yet.")

if __name__ == "__main__":
    main()