from typing import Any, Dict, List

from docutils import nodes
from docutils.parsers import rst as RST

import sphinx
from sphinx.application import Sphinx
from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator

####################### PART I: RST/DOCUTILS SIDE #######################


class jinja_div_node(nodes.General, nodes.Element):
    pass


class JinjaDiv(RST.Directive):
    """
    Maps source RST to a <jinja_div_node> doctree node.

    Example rst:
     .. jinja_div:: 203923
        :class: jj_class

        var1 var2

    Resulting doctree node:
        <jinja_div_node classes="jinja jj_class" ids="203923">
            <paragraph>var1 var2</paragraph>
        </jinja_div_node>

    """
    node_class = jinja_div_node
    optional_arguments = 1
    option_spec = {
        'id': RST.directives.unchanged,
        'class': RST.directives.unchanged
    }
    has_content = True

    def run(self) -> List[nodes.Node]:
        """Create doctree <jinja_div_node> from rst/myst source"""
        self.options['class'] = ['jinja ' + self.options.get('class', '')]
        RST.roles.set_classes(self.options)
        if self.arguments:
            self.options['ids'] = [self.arguments[0]]
        if self.has_content:
            text = '\n'.join(self.content)
        else:
            text = ''
        doctree_node = jinja_div_node(text, **self.options)
        self.add_name(doctree_node)
        self.state.nested_parse(self.content, self.content_offset, doctree_node)
        return [doctree_node]


####################### PART II: SPHINX/HTML SIDE #######################


def visit_jinja_div(self: HTMLTranslator, node: jinja_div_node) -> None:
    """
    Maps <jinja_div_node> doctree element to the html output.

    Example html output (example doctree node in the directive):
           <div id="293823" class="jinja jj_class"> >{{ var1 var2 }}</div>

    Note: if you can get at it, it's probably "cleaner" (???) to define these methods in a
    (sub-sub-)subclass of HTMLTranslator (eg, BootstrapHTML5Translator).

    """
    if node.children:
        txt = node.children[0].astext()
    node.remove(node.children[0])

    # self.starttag is defined in docutils.writers.HTML5Translator
    self.body.append(
        self.starttag(node, 'div') + ('{{ %s }}' % txt)
    )
    self.body.append('</div>')


def depart_jinja_div(self: HTMLTranslator, node: jinja_div_node) -> None:
    pass


def latex_visit_jinja_div(self: LaTeXTranslator, node: jinja_div_node) -> None:
    node.pop(0)


def latex_depart_jinja_div(self: LaTeXTranslator, node: jinja_div_node) -> None:
    pass


def setup(app: Sphinx) -> Dict[str, Any]:
    """ Add new doctree node definition to Sphinx, then add html & latex translators for that node. """ 
    app.add_node(jinja_div_node,
                 html=(visit_jinja_div, depart_jinja_div),
                 latex=(latex_visit_jinja_div, latex_depart_jinja_div),
                 text=(visit_jinja_div, depart_jinja_div),
                 man=(visit_jinja_div, depart_jinja_div),
                 texinfo=(visit_jinja_div, depart_jinja_div))

    app.add_directive('jinja_div', JinjaDiv)

    return {
        'version': sphinx.__display_version__,
    }
