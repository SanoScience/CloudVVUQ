import sys
import numpy as np
import json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: beam.py input_file")

    json_input = sys.argv[1]
    with open(json_input, 'r') as fd:
        inputs = json.load(fd)

    F = inputs['F']
    L = inputs['L']
    a = inputs['a']
    D = inputs['D']
    d = inputs['d']
    E = inputs['E']
    b = L - a
    I = np.pi * (D ** 4 - d ** 4) / 32.0
    g1 = -F * ((a ** 2 * (L - a) ** 2) / (3.0 * E * L * I))
    g2 = -F * ((b * (L ** 2 - b ** 2)) / (6.0 * E * L * I))
    g3 = F * ((a * (L ** 2 - a ** 2)) / (6.0 * E * L * I))

    outfile = inputs['outfile']
    with open(outfile, 'w') as fd:
        json.dump({'g1': g1, 'g2': g2, 'g3': g3}, fd)
