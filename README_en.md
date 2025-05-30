
# Player Evolution Analysis Project for Laghaim New

## 🎮 Context

This project analyzes the **evolution of characters in the MMORPG Laghaim New**, a private server maintained by a friend, with the goal of improving players' experience based on real gameplay data.

The business question guiding the work is:
> **How do players evolve, adapt to the server, and what improvements can be made to the gaming experience?**

---

## 🔍 Project Stages

1. **Data Collection**  
   Extracted data from server logs (`.log`), which include login time, character ID, level, and playtime information.

2. **Data Processing with Python**  
   - Used **regular expressions** to extract:
     - Date/time of login.
     - Character ID (CI).
     - Character level (CL).
   - Transformed this data into a **Pandas DataFrame**.
   - Divided data into **2-hour intervals** for time-based analysis.
   - Mapped each level to its corresponding **leveling map** using data from `mapas.xlsx`.

3. **Level Expansion**  
   Logs only contain snapshots of levels, not all incremental level-ups.  
   Applied a custom function `expand_levels` to infer and fill in missing levels between snapshots.

4. **SQLite Integration**  
   Loaded data into an **in-memory SQLite database**.  
   Used advanced SQL queries (`CTEs`, `LAG`) to:
   - Calculate daily average levels.
   - Summarize level progression in 2-hour intervals.
   - Count the number of active players per date.

5. **Excel Report Generation**  
   Loaded results into an existing Excel report (`relatorio_up.xlsx`) using `openpyxl`.  
   Final report includes:
   - Daily level progression (`Dados_Daily_Mean`).
   - Interval-based level evolution (`Dados_Interval_Mean`).
   - Number of active players (`Dados_Amount_Players`).

---

## 📁 Project Structure

```
├── mainfile.py                  # Main script: ETL pipeline and report generation
├── Laghaim_1_0_660.log          # Example server log
├── mapas.xlsx                   # Level intervals for leveling maps
├── relatorio_up.xlsx            # Final Excel report
├── support_functions_analysis.py# Custom support functions (e.g., expand_levels)
├── sqlit3_queries.py            # SQL queries for in-memory analysis
└── README.md                    # This file
```

---

## 🔧 Technologies Used

- **Python 3**: Data processing and automation.
- **pandas, numpy, re**: Data cleaning and transformation.
- **sqlite3 (memory)**: Fast, ad-hoc SQL analysis.
- **openpyxl**: Update existing Excel files.
- **Oracle Database** (for extended testing and storage).
- **Excel**: Final report delivery.

---

## 📈 Expected Outcomes

- **Identify periods** (by date and hour) with the highest player activity and evolution.
- **Understand leveling patterns** for each character.
- **Suggest adjustments** to XP balancing, events, or in-game buffs during strategic periods to improve retention and engagement.

---

## 🤝 Contribution

This project is a **learning lab** for data analysis in online games.  
Feel free to open *issues* or *pull requests* for improvements or suggestions!

---

### Updates from the Last Script
✅ Added direct **level interval mapping** from `mapas.xlsx`.  
✅ Implemented **level expansion logic** for more accurate progression tracking.  
✅ Reports are now automatically updated in `relatorio_up.xlsx` without needing to recreate the file.  
