import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: Read data from Excel file
excel_file = 'Types of Revision Survey(1-12).xlsx'  # Replace with your file name
sheet_name = 'Sheet1'     # Replace with your sheet name if necessary

# Load the data into a pandas DataFrame
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Step 2: Process text data
# Assuming we want to create a word cloud from a column named 'Text'
text_data = ' '.join(df['In general, what is your favourite method of revision? (e.g. making and using flashcards, long-form videos such as "ALL OF ALEVEL MATHS IN ONE VIDEO")'].dropna().astype(str))

# Step 3: Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

# Step 4: Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # No axes for this plot
plt.show()
