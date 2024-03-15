import subprocess
import json
import graph
import networkx as nx
import matplotlib.pyplot as plt
import visualization
def run_spider():
    subprocess.run(['scrapy', 'crawl', 'courses', '-O', 'courses.json', '--nolog'], capture_output=True, cwd='./course')


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



if __name__ == '__main__':
    #run_spider()
    directed_graph = graph.DirectdGraph()
    undirected_graph = graph.Graph()
    courses = read_file('./course/courses.json', directed_graph, undirected_graph)
    transfer_to_graphs(courses, directed_graph, undirected_graph)
    print(directed_graph.see_pre('STA314H1'))
    print(undirected_graph.get_exc('STA314H1'))
    visualization.visualize_graph(undirected_graph)
