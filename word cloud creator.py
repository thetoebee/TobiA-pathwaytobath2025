import pandas 
from wordcloud import WordCloud
import matplotlib.pyplot 

# Read data from Excel file
excel_file = 'Types of Revision Survey(1-12).xlsx'  
sheet_name = 'Sheet1'     

# Load the data into a pandas DataFrame (df)
df = pandas.read_excel(excel_file, sheet_name=sheet_name) 

# Processing text data
text_data = ' '.join(df['In general, what is your favourite method of revision? (e.g. making and using flashcards, long-form videos such as "ALL OF ALEVEL MATHS IN ONE VIDEO")'].dropna().astype(str))

# Generating the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)

#Displaying the word cloud
matplotlib.pyplot .figure(figsize=(10, 5))
matplotlib.pyplot .imshow(wordcloud, interpolation='bilinear')
matplotlib.pyplot .axis('off')  
matplotlib.pyplot.show()
