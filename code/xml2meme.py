import xml.etree.ElementTree as ET

def parse_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    motifs = []
    for motif in root.findall('.//motif'):
        id = motif.get('id')
        width = motif.get('width')
        sites = motif.get('sites')
        matrix = []
        for row in motif.findall('.//probabilities/alphabet_matrix/alphabet_array'):
            probs = [float(p.text) for p in row.findall('.//value')]
            matrix.append(probs)
        motifs.append((id, width, sites, matrix))

    return motifs

def write_meme(motifs, filename):
    with open(filename, 'w') as f:
        f.write('MEME version 4\n')
        f.write('\nALPHABET= ACGT\n')
        f.write('\nstrands: + -\n')
        f.write('\nBackground letter frequencies\n')
        f.write('A 0.25 C 0.25 G 0.25 T 0.25\n')

        for id, width, sites, matrix in motifs:
            f.write(f'\nMOTIF {id}\n')
            f.write(f'letter-probability matrix: alength= 4 w= {width} nsites= {sites} E= 0\n')
            for row in matrix:
                f.write(' '.join(f'{p:.6f}' for p in row))
                f.write('\n')

# Usage:
motifs = parse_xml('meme.xml')
write_meme(motifs, 'meme.meme')
