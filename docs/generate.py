import os
def build():
    os.system("""
    sphinx-apidoc -o source ../neonize
    make html
    """)