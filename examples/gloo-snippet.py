# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import gloo

A = gloo.Snippet("uniform float a;\nvoid function_A(void) {};\n\n", name = "Snippet_A")
B = gloo.Snippet("uniform float b;\nvoid function_B(void) {};\n\n", name = "Snippet_B")
C = gloo.Snippet("uniform float c;\nvoid function_C(void) {};\n\n", name = "Snippet_C")
D = A(B("P")) + C()

print("D:             ", D)
print("D['Snippet_A']:", D["Snippet_A"])
print("D['Snippet_B']:", D["Snippet_B"])
print("D['Snippet_C']:", D["Snippet_C"])

print()
print("D.locals: ", D.locals)
print("D.globals:", D.globals)
print("D['Snippet_A'].locals:", D["Snippet_A"].locals)
print("D['Snippet_B'].locals:", D["Snippet_B"].locals)
print("D['Snippet_C'].locals:", D["Snippet_C"].locals)
print("D.symbols:", D.symbols)
print()

# print D.objects

#print(D)
#print([snippet._id for snippet in D.dependencies])

print("Call:")
print(D.call)
print()
print("Code:")
print(D.code)
print()
