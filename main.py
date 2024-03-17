import subprocess
import json
import graph
import gui
import tkinter as tk


def run_spider():
    subprocess.run(['scrapy', 'crawl', 'courses', '-O', 'courses1.json', '--nolog'], capture_output=True,
                   cwd='./course')


mode = 1


def read_file(file_name: str, directed: graph.DirectdGraph, undirected: graph.Graph) -> dict:
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
        c = graph.Course(code, title, introduction, br, pre, exc, distribution)
        coursess[code] = c
        directed.add_vertex(code)
        undirected.add_vertex(code)
    return coursess


def transfer_to_graphs(coursess: dict[str:graph.Course], directed: graph.DirectdGraph, undirected: graph.Graph):
    for c in coursess.values():
        code = c.code
        pre = c.pre
        exc = c.exc
        for exclusion in exc:
            undirected.add_edge(exclusion, code)
        for prerequisite in pre:
            directed.add_arc(prerequisite, code)
    return coursess


def initialization(mode=0):
    directed_graph = graph.DirectdGraph()
    undirected_graph = graph.Graph()
    if mode == 0:
        run_spider()
        courses = read_file('./course/courses1.json', directed_graph, undirected_graph)
    else:
        courses = read_file('./course/courses.json', directed_graph, undirected_graph)
    course = transfer_to_graphs(courses, directed_graph, undirected_graph)
    return directed_graph, undirected_graph, course


def start():
    global mode
    mode_set = tk.Tk()
    mode_set.title("CourseMaster")
    mode_set.geometry('300x300')
    selected_option = tk.StringVar(value='use the default dataset')
    options = ["use the default dataset", "update now(takes longer time)"]
    for option in options:
        tk.Radiobutton(mode_set, text=option, variable=selected_option, value=option).pack(anchor=tk.W)

    def c():
        global mode
        if selected_option.get() == 'use the default dataset':
            mode = 1
            mode_set.destroy()
        else:

            mode = 0
            mode_set.destroy()

    b = tk.Button(mode_set, text='OK', command=c)
    b.pack()
    mode_set.mainloop()


# new=tk.Tk()
# new.geometry('300x400')
# options = ["small", "medium", "large"]
# selected_option = tk.StringVar(value='medium')
# for option in options:
#     tk.Radiobutton(new, text=option, variable=selected_option, value=option).pack()
# def vis1():
#     print(selected_option.get())
#     # if self.selected_option == 'small':
#     #     a = 50
#     # elif self.selected_option.get() == 'medium':
#     #     a = 500
#     # else:
#     #     a = 50000
#     # print(self.selected_option.get())
#     # visualization.visualize_graph(self.undirected_graph,max_vertices=a)
# l= tk.Label(new, textvariable=selected_option)
# l.pack()
# b = tk.Button(new, text='Visualize', command=vis1)
# b.pack()
# new.mainloop()

if __name__ == '__main__':
    # # run_spider()
    # directed_graph = graph.DirectdGraph()
    # undirected_graph = graph.Graph()
    # courses = read_file('./course/courses.json', directed_graph, undirected_graph)
    # transfer_to_graphs(courses, directed_graph, undirected_graph)
    # # print(directed_graph.see_pre('STA314H1'))
    # # print(undirected_graph.get_exc('STA314H1'))
    # # visualization.visualize_graph(undirected_graph)

    start()
    directed_graph, undirected_graph, courses = initialization(mode)
    main = gui.MainWindow(800, 700, undirected_graph, directed_graph, courses)
    main.mainloop()