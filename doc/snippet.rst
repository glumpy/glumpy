========
Snippets
========

A snippet is a piece of GLSL code that can be injected into an another GLSL
code. It provides the necessary machinery to take care of name collisions,
external variables and snippet composition (call, +, -, /, \*).

A snippet can declare uniforms, const, attributes and varying using random
names. However, these names will be later mangled such as to avoid name
collisions with other snippets and/or main code. This means that any snippet
variable must be accessed through the snippet (snippet["variable"]) to be able
to change its value within the main program.

Creation
========

Let's consider a simple piece of code:

.. code:: C

   uniform float alpha;
   vec4 process(vec3 color)
   {
       return vec4(0,0,0,alpha);
   }

Not very interesting code but it will serve our purpose. To create a snippet


Transforms
==========
