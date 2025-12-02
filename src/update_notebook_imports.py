import json
import os

nb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks', 'analysis.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'from data_loader import FitFamDataLoader' in source:
            new_source = [
                "import pandas as pd\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import numpy as np\n",
                "import sys\n",
                "import os\n",
                "# Add src to path to import data_loader\n",
                "sys.path.append(os.path.abspath('../src'))\n",
                "from data_loader import FitFamDataLoader\n",
                "\n",
                "%matplotlib inline\n",
                "sns.set_style('whitegrid')\n",
                "plt.rcParams['figure.figsize'] = (12, 6)\n",
                "# Set font for Chinese characters\n",
                "plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']\n",
                "plt.rcParams['axes.unicode_minus'] = False"
            ]
            cell['source'] = new_source
            print("Updated imports in notebook.")
            break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
