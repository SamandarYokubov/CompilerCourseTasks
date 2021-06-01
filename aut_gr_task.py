from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from graphviz import Digraph
import welcomescreen


class AutomataGrammarTask(QDialog):
    def __init__(self,widget):
        super(AutomataGrammarTask, self).__init__()
        loadUi('gui/automata_grammar_task.ui', self)
        self.widget=widget
        self.automata = Digraph(format='png')
        self.nodes_edges = {}
        self.difference_index = 0
        self.add_edge_btn.clicked.connect(self.add_edge)
        self.solve_btn.clicked.connect(self.get_grammar)
        self.del_btn.clicked.connect(self.delete)
        self.back_button.clicked.connect(self.back_to_menu)
        self.back_button.setIcon(QtGui.QIcon('icons/back.png'))
        self.back_button.setIconSize(QtCore.QSize(30, 30))

    def back_to_menu(self):
        welcome = welcomescreen.WelcomeScreen(self.widget)
        self.widget.addWidget(welcome)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    def delete(self):
        del self.automata
        self.automata = Digraph(format='png')
        self.automata.render('graphs/grammar', view=False)
        automata_image = QPixmap('graphs/grammar.png')
        self.automata_output.setPixmap(automata_image)
        self.automata_output.setAlignment(Qt.AlignCenter)
        self.grammar_output.clear()

    def get_grammar(self):
        self.grammar = ''
        for head in self.nodes_edges.keys():            
            if  self.nodes_edges[head]:
                self.grammar += (head+'->')
                for body in self.nodes_edges[head]:
                    self.grammar += (body+'|')
                self.grammar = self.grammar[:-1]
                self.grammar += '\n'
        self.grammar_output.setText(self.grammar)

    def add_edge(self):
        out_node = self.out_node.text()
        in_node = self.in_node.text()
        edge_label = self.edge_label.text()
        if out_node != '':
            if out_node not in self.nodes_edges.keys():
                self.nodes_edges[out_node] = []
                self.automata.node(out_node)
            if in_node != '':
                if in_node not in self.nodes_edges.keys():
                    self.nodes_edges[in_node] = []
                    self.automata.node(in_node)
                if edge_label != '' and edge_label != 'lambda':
                    if (edge_label+in_node) not in self.nodes_edges[out_node]:
                        self.automata.edge(out_node, in_node, label=edge_label)
                        self.nodes_edges[out_node].append(edge_label+in_node)
                    else:
                        welcomescreen.execute_message_box("This edge already exists","Input Data Warning")
                        return
                else:
                    welcomescreen.execute_message_box("Wrong input data","Input Data Warning")
                    return
            elif edge_label == 'lambda':
                if edge_label not in self.nodes_edges[out_node]:
                    self.automata.node(
                        str(self.difference_index), '', shape='none')
                    self.automata.node(out_node, color='blue')
                    self.automata.edge(out_node, str(
                        self.difference_index), color='blue')
                    self.nodes_edges[out_node].append('lambda')
                    self.difference_index += 1
                else:
                    welcomescreen.execute_message_box("This edge already exists","Input Data Warning")
                    return
            elif edge_label.isdigit():
                if edge_label not in self.nodes_edges[out_node]:
                    self.automata.node('f'+str(self.difference_index),
                                    '', shape='circle', color='blue')
                    self.automata.edge(
                        out_node, 'f'+str(self.difference_index), label=edge_label)
                    self.automata.node(
                        str(self.difference_index), '', shape='none')
                    self.automata.edge('f'+str(self.difference_index),
                                    str(self.difference_index), color='blue')
                    self.nodes_edges[out_node].append(edge_label)
                    self.difference_index += 1
                else:
                    welcomescreen.execute_message_box("This edge already exists","Input Data Warning")
                    return
            else:
                welcomescreen.execute_message_box("Wrong input data","Input Data Warning")
                return
        else:
            welcomescreen.execute_message_box("Wrong input data","Input Data Warning")
            return

        self.out_node.clear()
        self.in_node.clear()
        self.edge_label.clear()
        self.automata.render('graphs/grammar', view=False)
        automata_image = QPixmap('graphs/grammar.png')
        self.automata_output.setPixmap(automata_image)
        self.automata_output.setAlignment(Qt.AlignCenter)