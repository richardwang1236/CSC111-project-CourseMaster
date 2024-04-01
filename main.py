"""
These are the modules we will be using for main.py
"""
import subprocess
import json
import tkinter as tk
import graph
import gui


class CourseMaster:
    """
    A class to represent the CourseMaster program
    """
    mode: int

    def __init__(self) -> None:
        self.mode = 1

    def run_spider(self) -> None:
        """
        Run the scrappy spider to crawl the data from the website
        """
        subprocess.run(['scrapy', 'crawl', 'courses', '-O', 'courses1.json', '--nolog'], capture_output=True,
                       cwd='./course')

    def read_file(self, file_name: str, directed: graph.DirectdGraph, undirected: graph.Graph) -> dict:
        """
        Read the courses.json file and return a dictionary of courses
        """
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        coursess = {}
        for a in data:
            code = a['name'][0:10].strip()
            title = a['name'][13:].strip()
            introduction = ''.join(a['introduction'])
            br = a['br']
            pre = a['pre']
            exc = a['exclusion']
            distribution = a['distribution']
            coursess[code] = graph.Course(code, title, introduction, br, pre, exc, distribution)
            directed.add_vertex(code)
            undirected.add_vertex(code)
        return coursess

    def transfer_to_graphs(self, courses1: dict[str:graph.Course], direct: graph.DirectdGraph,
                           undirect: graph.Graph) -> dict[str:graph.Course]:
        """
        Transfer the courses to the directed and undirected graphs
        """
        for c in courses1.values():
            code = c.code
            pre = c.pre
            exc = c.exc
            for exclusion in exc:
                undirect.add_edge(exclusion, code)
            for prerequisite in pre:
                direct.add_arc(prerequisite, code)
        return courses1

    def initialization(self, method: int = 0) -> tuple[graph.DirectdGraph, graph.Graph, dict[str:graph.Course]]:
        """
        Initialize the program by reading the data from the file and transfer the data to the graphs
        """
        d_graph = graph.DirectdGraph()
        u_graph = graph.Graph()
        if method == 0:
            self.run_spider()
            all_courses = self.read_file('./course/courses1.json', d_graph, u_graph)
        else:
            all_courses = self.read_file('./course/courses.json', d_graph, u_graph)
        course = self.transfer_to_graphs(all_courses, d_graph, u_graph)
        return d_graph, u_graph, course

    def start(self) -> None:
        """
        Sets the mode of the program by asking the user to choose between using the default dataset or updating
        the dataset.
        """
        mode_set = tk.Tk()
        mode_set.title("CourseMaster")
        mode_set.geometry('300x100')
        selected_option = tk.StringVar(value='Use the Default Data Set')
        options = ["Use the Default Data Set", "Update Data Set (This may take a while)"]
        for option in options:
            tk.Radiobutton(mode_set, text=option, variable=selected_option, value=option).pack(anchor=tk.W)

        def c() -> None:
            """
            Set the mode of the program
            """
            if selected_option.get() == 'Use the Default Data Set':
                self.mode = 1
                mode_set.destroy()
            else:

                self.mode = 0
                mode_set.destroy()

        b = tk.Button(mode_set, text='Confirm', command=c)
        b.pack()
        mode_set.mainloop()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['subprocess', 'json', 'tkinter', 'graph', 'gui'],  # the names (strs) of imported modules
        'allowed-io': ['CourseMaster.read_file'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })

    course_master = CourseMaster()
    course_master.start()
    directed_graph, undirected_graph, courses = course_master.initialization(course_master.mode)
    main = gui.MainWindow(500, undirected_graph, directed_graph, courses)
    main.mainloop()
