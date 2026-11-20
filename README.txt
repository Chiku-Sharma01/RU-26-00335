POPULATION DATA VISUALIZER - PS NO. 21
Python 3 | First Semester Project

FILES
- population_visualizer.py: main Python program
- population.csv: sample data (dummy data only)
- requirements.txt: required libraries

HOW TO RUN IN VS CODE (Windows)
1. Extract this ZIP file.
2. Open the Population_Data_Visualizer folder in VS Code.
3. Open Terminal in VS Code (Terminal > New Terminal).
4. Check Python: python --version
5. Install libraries once:
   python -m pip install -r requirements.txt
6. Run the project:
   python population_visualizer.py
7. Choose:
   1 = population summary
   2 = growth and charts
   3 = exit

CSV COLUMNS
City, Year, Population

NOTES
- Keep population.csv and population_visualizer.py in the same folder.
- If the terminal says a library is missing, run the install command again.
- The program cleans the data when it loads the file: rows with an invalid
  or non-positive Population are skipped and duplicate City/Year rows are removed.
- To test another CSV file, give its name after the program name:
  python population_visualizer.py test3.csv
- Growth % = (latest - earliest) / earliest x 100.
- If a city has only one year of data, growth is shown as not available.
- Option 2 shows two charts: bar chart "Population Growth by City" and
  line chart "Population Trend". Close each chart window to continue.
