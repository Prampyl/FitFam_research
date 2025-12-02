import json
import os

nb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks', 'analysis.ipynb')

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Category Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Top Categories by Attendance\n",
    "cat_counts = df['category_name'].value_counts().head(10)\n",
    "plt.figure(figsize=(12, 6))\n",
    "sns.barplot(x=cat_counts.values, y=cat_counts.index)\n",
    "plt.title('Top 10 Categories by Attendance')\n",
    "plt.xlabel('Number of Check-ins')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Categories by City (Top 3 Cities)\n",
    "top_cities = df['city_name'].value_counts().head(3).index\n",
    "df_top_cities = df[df['city_name'].isin(top_cities)]\n",
    "\n",
    "plt.figure(figsize=(14, 8))\n",
    "sns.countplot(y='category_name', hue='city_name', data=df_top_cities, order=df_top_cities['category_name'].value_counts().iloc[:10].index)\n",
    "plt.title('Top Categories in Major Cities')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Gender Distribution by Category (Top 5 Categories)\n",
    "top_cats = df['category_name'].value_counts().head(5).index\n",
    "df_top_cats = df[df['category_name'].isin(top_cats)]\n",
    "\n",
    "plt.figure(figsize=(12, 6))\n",
    "sns.countplot(x='category_name', hue='gender_label', data=df_top_cats)\n",
    "plt.title('Gender Distribution by Top Categories')\n",
    "plt.xticks(rotation=45)\n",
    "plt.show()"
   ]
  }
]

# Check if cells already exist to avoid duplication
existing_sources = [''.join(c['source']) for c in nb['cells']]
if "## 5. Category Analysis" not in existing_sources:
    nb['cells'].extend(new_cells)
    print("Added category analysis cells.")
else:
    print("Category analysis cells already exist.")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
