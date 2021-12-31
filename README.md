# Minimal Sphinx extension: embed Jinja expressions in Sphinx-generated HTML
In general terms, this extension shows:
1. How to define an new RST directive and add it to Sphinx.
1. Given that directive, how to define and generate a new docutils node from it.
1. Finally, how to produce HTML output from this docutils node.

Rationale: documented examples elsewhere (eg, the todo/todolist example in sphinx.ext) have more functional depth, but also more dependencies on other parts of the 
Sphinx ecosystem (eg, admonition, container). I couldn't find a real **minimal** example, so I hope this serves as one.

Use case for this specific extension: use documents produced by Sphinx as Jinja templates 
that get rendered by a Flask application. For this, we need a directive that translates into "{{ var1 var2 }}" blocks in our html output.
Note: this is completely independent of the *internal* use of Jinja by Sphinx.

## Installation

### Install Sphinx and create a project 

Create a fresh python environment
~~~~
  conda create -n jinja_ext python
  conda activate jinja_ext
~~~~

Install sphinx as per the [Sphinx Getting Started](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html):
~~~~
  pip install sphinx

  mkdir myproj        # or whatever you like
  cd myproj
  mkdir docs
  cd docs

  sphinx-quickstart   # answer 'no' to the option of separate source and build dirs
  make html
~~~~
You should now have a Sphinx-generated html file in the _build/html directory.

### Install and test extension

Install the extension (also see [Sphinx extensions docs](https://www.sphinx-doc.org/en/master/usage/extensions/index.html#where-to-put-your-own-extensions) )
~~~~
  # assuming you're still in myproj/docs
  git clone https://github.com/kleynjan/sphinx-jinja-ext.git

  # in conf.py:
  import sys, os
  sys.path.append(os.path.abspath('sphinx-jinja-ext'))
  extensions = ['jinja']
  ~~~~

Add a jinja_div directive to the index.rst source file, for instance below the ..toctree:
~~~~
  [...toctree stuff...]

  This paragraph will be followed by a jinja div.

  .. jinja_div:: 203923
     :class: jj_class

     var1 var2

  And this concludes our jinja show for today.
  Resuming normal programming now!
~~~~

Make html & look at the results
~~~~
  make clean
  make html
~~~~
In the generated index.html in the _build/html directory, the div element has been added:
~~~~
  <div class="jinja jj_class" id="203923">
    {{ var1 var2 }}
  </div>
~~~~

### **Bonus**: Markdown syntax
Also see [MyST install](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html#using-markdown-with-sphinx)
~~~~
  pip install myst-parser
  # and in config.py:
  extensions = ['myst_parser','jinja']
~~~~
Create a new markdown file named index2.md:
~~~~
  # Testing one two three

  Paragraph before the div...
  ```{jinja_div} 203923
  ---
  class: jj_class
  ---
  var1 var2
  ```
  Paragraph after the div.
~~~~
Run make build again and examine the resulting index2.html.

### Finally

**Tip.** If you need to debug the steps from RST/MD to docutils to HTML, I've found it useful to examine the generated intermediate docutils nodes. The included script is just a wrapper, it 
unpickles the doctree and generates pretty xml:
~~~~
  cd sphinx-jinja-ext
  chmod +x dt2xml.py
  ./dt2xml.py ../_build/doctrees/index
~~~~
Open up ../_build/doctrees/index.xml and you'll see the doctree nodes:
~~~~
  <paragraph>This paragraph will be followed by a jinja div.</paragraph>
  <jinja_div_node classes="jinja\ jj_class" ids="203923">
      <paragraph>var1 var2</paragraph>
  </jinja_div_node>
  <paragraph>And this concludes our jinja show for today.
~~~~

Hope this helps. A big thank you to the [Executable Book Project](https://executablebooks.org) for their excellent tools and
documentation!
