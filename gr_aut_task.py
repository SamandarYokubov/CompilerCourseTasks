from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from graphviz import Digraph
import welcomescreen


class Node:
    def __init__(self, node):
        self.node = node
        self.out_edges = {}

    def add_edge(self, to_node, label):
        if to_node not in self.out_edges.keys():
            self.out_edges[to_node] = ''
        self.out_edges[to_node] += (label+',')


class GrammarAutomataTask(QDialog):
    def __init__(self,widget):
        super(GrammarAutomataTask, self).__init__()
        loadUi('gui/grammar_automata_task.ui', self)
        self.widget=widget
        self.back_btn.clicked.connect(self.back_to_menu)
        self.back_btn.setIcon(QtGui.QIcon('icons/back.png'))
        self.back_btn.setIconSize(QtCore.QSize(30, 30))
        self.solve_btn.clicked.connect(self.get_automata)
        self.reset.clicked.connect(self.reset_text)
        self.add_production_btn.clicked.connect(self.add_production)

    def add_production(self):
        head = self.head_le.text()
        body = self.body_le.text()
        production = head+'->'+body
        self.grammar_input.append(production)
        self.head_le.clear()
        self.body_le.clear()

    def reset_text(self):
        self.grammar_input.clear()
        self.automata_output.clear()

    def back_to_menu(self):
        welcome = welcomescreen.WelcomeScreen(self.widget)
        self.widget.addWidget(welcome)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    def get_automata(self):
        input_data = self.grammar_input.toPlainText()
        if input_data != '':
            nodes_and_edges = self.parse_grammar(input_data)
            self.build_automata(nodes_and_edges)
        else:
            welcomescreen.execute_message_box("Enter input data","Input Data Warning")
            return

    def parse_grammar(self, grammar):
        nodes = {}
        productions = grammar.split('\n')
        for production in productions:
            production_items = production.split('->')
            head = production_items[0]
            bodies = production_items[1].split('|')
            if head not in nodes.keys():
                nodes[head] = Node(head)
            output_bodies = ''
            for body in bodies:
                if len(body) == 1:
                    output_bodies += (body+',')
                elif body == 'lambda':
                    nodes[head].add_edge('None', '')
                else:
                    if self.left_body.isChecked():
                        nodes[head].add_edge(body[:-1], body[-1])
                    else:                        
                        nodes[head].add_edge(body[1:], body[0])
            if output_bodies != '':
                nodes[head].add_edge('Finals', output_bodies[:-1])

        return nodes

    def build_automata(self, nodes_and_edges):
        automata = automata = Digraph(format='png')
        nodes = nodes_and_edges.keys()
        index_for_difference = 0
        for node in nodes:
            automata.node(node)
        for node in nodes:
            to_nodes = nodes_and_edges[node].out_edges.keys()
            for to_node in to_nodes:
                if to_node == 'None':
                    automata.node(node, color='blue')
                    automata.node(str(index_for_difference), '', shape='none')
                    automata.edge(
                        node, str(index_for_difference), color='blue')
                elif to_node == 'Finals':
                    automata.node('f'+str(index_for_difference),
                                  '', shape='circle', color='blue')
                    automata.edge(node, 'f'+str(index_for_difference),
                                  label=nodes_and_edges[node].out_edges[to_node][:-1])
                    automata.node(str(index_for_difference), '', shape='none')
                    automata.edge('f'+str(index_for_difference),
                                  str(index_for_difference), color='blue')
                else:
                    automata.edge(
                        node, to_node, label=nodes_and_edges[node].out_edges[to_node][:-1])
                index_for_difference += 1
        automata.render('graphs/grammar_to_automata', view=False)
        automata_image = QPixmap('graphs/grammar_to_automata.png')
        self.automata_output.setPixmap(automata_image)
        self.automata_output.setAlignment(Qt.AlignCenter)