import tkinter as tk
import visualization


class MainWindow(tk.Tk):
    """
    The main window of the GUI, which contains three buttons for three functions: visualization for exclusion,
    statistics, and course search. The visualization for exclusion button will open a new window for the user to choose
    the size of the graph to visualize. The statistics button will open a new window to display the statistics of the
    courses, including the number of courses in each campus, the number of courses in each distribution, and the number
    of courses in each breadth requirement. The course search button will open a new window for the user to search for a
    course by its code, and the window will display the search result and the details of the course if the search result
    is a single course. The user can also visualize the exclusion relationship of the course by clicking the "vis_exc"
    button.
    """

    def __init__(self, height, width, undirected_graph, directedgraph, courses):
        """
        Initialize the main window of the GUI.
        """
        super().__init__()
        self.text5 = None
        self.text4 = None
        self.text3 = None
        self.entry = None
        self.text = None
        self.selected_option1 = None
        self.text_long = None
        self.text_short = None
        self.selected_option = None
        self.courses = courses
        self.directedgraph = directedgraph
        self.undirected_graph = undirected_graph
        self.geometry(f'{height}x{width}')
        self.label = tk.Label(self, text='Course Master', font=("Helvetica", 50))
        self.label.pack()
        self.title('CourseMaster')
        self.button = tk.Button(self, text='visualization for exclusion', command=self.button_click)
        self.button.pack()
        self.button1 = tk.Button(self, text='statistic', command=self.button_click1)
        self.button1.pack()
        self.button3 = tk.Button(self, text='course search', command=self.button_click3)
        self.button3.pack()

    def button_click(self):
        """
        Open a new window for the user to choose the size of the graph to visualize.
        """
        new = tk.Tk()
        new.geometry('300x400')
        new.title('Visualization for exclusion')
        options = ["small", "medium", "large"]
        self.selected_option = tk.StringVar(new)
        self.selected_option.set(options[1])
        for option in options:
            tk.Radiobutton(new, text=option, variable=self.selected_option, value=option).pack()
        b = tk.Button(new, text='Visualize', command=self.vis1)
        b.pack()

    def button_click1(self):
        """
        Open a new window to display the statistics of the courses, including the number of courses in each campus, the
        number of courses in each distribution, and the number of courses in each breadth requirement.
        """
        new1 = tk.Tk()
        new1.geometry('500x500')
        new1.title('Statistics')
        course_utsg = [c for c in self.undirected_graph.get_vertices().values() if c.item[-1] == '1']
        course_utsc = [c for c in self.undirected_graph.get_vertices().values() if c.item[-1] == '3']
        course_utm = [c for c in self.undirected_graph.get_vertices().values() if c.item[-1] == '5']
        brs = [c.br for c in self.courses.values()]
        distribution = [c.distribution for c in self.courses.values()]
        science, humanities, social = 0, 0, 0
        br1, br2, br3, br4, br5 = 0, 0, 0, 0, 0
        for d in distribution:
            if d:
                if 'Science' in d[0]:
                    science += 1
                if 'Humanities' in d[0]:
                    humanities += 1
                if 'Social Science' in d[0]:
                    social += 1
        for br in brs:
            if br:
                if '1' in br[0]:
                    br1 += 1
                if '2' in br[0]:
                    br2 += 1
                if '3' in br[0]:
                    br3 += 1
                if '4' in br[0]:
                    br4 += 1
                if '5' in br[0]:
                    br5 += 1
        course_counts = len(course_utsg) + len(course_utsc) + len(course_utm)
        self.text_short = (
            f"Among the three campus of the university of toronto, there are {course_counts} courses in total. "
            f"Science Courses: {science}. Humanities Courses: {humanities}, Social Science Courses: {social} "
            f"br1: {br1}, br2: {br2}, br3: {br3}, br4: {br4},br5:{br5}")
        self.text_long = f"long"
        options = ["short text", "long text"]

        self.selected_option1 = tk.StringVar(new1)
        self.selected_option1.set(options[0])
        for option in options:
            tk.Radiobutton(new1, text=option, variable=self.selected_option1, value=option,
                           command=self.update_text).pack()
        self.text = tk.StringVar(new1)
        self.text.set(self.text_short)

        t = tk.Label(new1, textvariable=self.text, wraplength=400, font=("Helvetica", 15))
        t.pack()

    def update_text(self):
        """
        Update the text displayed in the statistics window based on the user's selection.
        """
        if self.selected_option1.get() == "short text":
            self.text.set(self.text_short)
        else:
            self.text.set(self.text_long)

    def vis1(self):
        """
        Visualize the exclusion relationship of all courses in the graph based on the user's selection of the size of
        the graph to visualize.
        """
        if self.selected_option.get() == 'small':
            a = 50
        elif self.selected_option.get() == 'medium':
            a = 1000
        else:
            a = 10000
        visualization.visualize_graph(self.undirected_graph, max_vertices=a, title=f'exclusion relationship for all '
                                                                                   f'courses ({a}) size')

    def search(self):
        """
        Search for a course by its code and display the search result and the details of the course if the search result
        is a single course.
        """
        query = self.entry.get().upper()
        result = [c for c in self.courses if query in c]

        if 1 < len(result) < 10:
            self.text3.set(f'Classes: {', '.join(result)}')
        elif len(result) == 1:
            self.text3.set(result[0])
        elif len(result) == 0:
            self.text3.set("No result")
        else:
            self.text3.set('Be more specific！')

        # beginning of detail
        if len(self.text3.get()) == 8:
            course = self.courses[self.text3.get()]
            br = course.br
            intro = course.introduction
            title = course.title
            dis = course.distribution
            text = f'{title}\n{intro}\ndistribution：{dis[0]}\nBreadth Req: {br[0]}'
            self.text4.set(text)
        else:
            text = 'Please narrow down your search to view details!'
            self.text4.set(text)
        # end of detail

    def button_click3(self):
        """
        Open a new window for the user to search for a course by its code and display the search result and the details
        of the course if the search result is a single course. The user can also visualize the exclusion relationship of
        the course by clicking the "vis_exc" button.
        """
        click3 = tk.Tk()
        click3.geometry('500x500')
        click3.title('Course Search')
        self.entry = tk.Entry(click3)
        self.text3 = tk.StringVar(click3, value='Search for a Class!')
        self.text4 = tk.StringVar(click3)
        self.text5 = tk.StringVar(click3)
        self.entry.pack()
        search_button = tk.Button(click3, text="Search", command=self.search)
        search_button.pack()
        show = tk.Label(click3, textvariable=self.text3, wraplength=400)
        show.pack()
        show1 = tk.Label(click3, textvariable=self.text4, wraplength=400)
        show1.pack()
        # detail = tk.Button(click3, text="detail", command=self.detail)
        # detail.pack()
        vis_exc = tk.Button(click3, text='vis_exc', command=self.exc)
        vis_exc.pack()
        show2 = tk.Label(click3, textvariable=self.text5, wraplength=400)
        show2.pack()

    def exc(self):
        """
        Visualize the exclusion relationship of the course based on the user's search result.
        """
        if len(self.text3.get()) == 8:
            text = 'Loading Graph...'
            self.text5.set(text)
            g = self.undirected_graph.get_exc(self.text3.get())
            visualization.visualize_graph(g, max_vertices=500, item=self.text3.get(),
                                          title=f'exclusion for {self.text3.get()}', layout='kamada_kawai_layout')
            text = 'Graph Loaded!'
            self.text5.set(text)
        else:
            text = 'Narrow your search to view exclusions!'
            self.text5.set(text)
