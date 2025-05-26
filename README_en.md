# Player Evolution Analysis Project for Laghaim New

## 🎮 Context

This project aims to analyze the **evolution of characters in the MMORPG Laghaim New**, a private server maintained by a friend, with the goal of improving the players' experience based on real gameplay data.

The business question that guided the work was:
> **How do players evolve to adapt the server and improve the gaming experience?**

## 🔍 Project Stages

1. **Data Collection**
   - Extracting server logs (`.log`) containing information about login, character ID, level, and playtime.

2. **Data Processing with Python**
   - I used regular expressions to extract `date/time`, `character ID (CI)`, and `level (CL)` from each valid log entry.
   - The data was transformed into a Pandas `DataFrame`.
   - Playtime data was grouped into 2-hour intervals for time-based analysis.

3. **Persistence and Analysis**
   - The data was temporarily stored in an in-memory SQLite database.
   - Complex SQL queries (using CTEs and `LAG`) were used to:
     - Calculate the max and min level per character per time interval.
     - Calculate evolution across time intervals.
     - Summarize the level progression of each character.

4. **Integration with Excel**
   - The final DataFrame was exported to an Excel sheet (`relatorio_up.xlsx`) using `openpyxl` for easier reading and presentation of the final report.

5. **Oracle Integration (outside the script)**
   - In additional tests, the data was integrated with an Oracle database for more robust SQL analysis and permanent storage.

## 📁 Project Structure

```
├── mainfile.py               # Main script for extraction, transformation, and loading
├── Laghaim_1_0_660.log       # Example server log
├── relatorio_up.xlsx         # Report with results (not included in public repo)
└── README.txt                # This file
```

## 🔧 Technologies Used

- Python 3
- pandas, numpy, re
- sqlite3 (memory)
- openpyxl
- Oracle DB (for advanced tests)
- Excel (output of results)

## 📈 Expected Results

Based on the log analysis:
- It's possible to identify the periods of the day with the highest player evolution activity.
- Detect usage patterns per character.
- Suggest adjustments in XP balancing, events, or buffs at strategic times.

## 🤝 Contribution

Feel free to open *issues* or *pull requests* with improvements or suggestions. This project is a lab for learning data analysis applied to online games. README_en.md…]()
