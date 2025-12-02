import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Path relative to src/
nb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks', 'analysis_output.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        if cell['outputs']:
            print(f"--- Cell Output ---")
            for output in cell['outputs']:
                output_type = output.get('output_type')
                if output_type == 'stream':
                    name = output.get('name', 'stdout')
                    text = ''.join(output['text'])
                    print(f"[{name}] {text}")
                elif output_type == 'error':
                    print(f"[ERROR] {output.get('ename')}: {output.get('evalue')}")
                    for line in output.get('traceback', []):
                        print(line)
                elif output_type in ('execute_result', 'display_data'):
                    data = output.get('data', {})
                    if 'text/plain' in data:
                        print(f"[DATA] {''.join(data['text/plain'])}")
