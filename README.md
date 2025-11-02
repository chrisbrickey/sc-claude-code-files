# ECommerce Analysis Refactored with Claude Code

This repository contains the resources from Lesson 7 of a short course "Claude Code: A highly Agentic Coding Assistant".
I forked this repository to practice using Claude Code to refactor a jupyter notebook and to generate from a web UI (from the notebook).

## Prerequisites

- Python 3.8 or higher
- This project uses `uv` for package management
- Virtual environment is located at `.venv/` in the project root

## QuickStart Guides

### Web UI QuickStart

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   uv pip install -r requirements.txt
   ```

3. **Start the dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

   Or run directly without activating the environment:
   ```bash
   .venv/bin/streamlit run dashboard.py
   ```

4. **Access the dashboard**:
   - The dashboard will automatically open in your default web browser
   - Default URL: `http://localhost:8501`

### Jupyter Lab QuickStart (alternative to using web UI)

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Launch Jupyter Lab**:
   ```bash
   jupyter lab
   ```

   Or run directly without activating the environment:
   ```bash
   .venv/bin/jupyter lab
   ```

3. **Open the notebook**:
   - Navigate to `notebooks/EDA_Refactored.ipynb` for the modular analysis framework
   - Or open `notebooks/EDA.ipynb` for the original exploratory analysis

## Dashboard Visualizations
- Monthly revenue trend line charts
- Top product category horizontal bar charts
- Interactive US state choropleth maps
- Customer satisfaction distribution charts

## Dashboard Usage

**Filters**
- **Year Filter**: Select the year to analyze (defaults to 2023 if available)
- **Month Filter**: Choose "All Months" for full-year analysis or select a specific month

**Metrics**
- **Monthly Growth**: Average month-over-month percentage change within selected year
- **Trend Indicators**: Year-over-year comparison with color-coded arrows
- **Revenue Formatting**: Automatic K/M suffixes for readability

**Charts**
- All visualizations update automatically when filters change
- Interactive Plotly charts with hover details
- Professional blue gradient color scheme
- Grid lines for easier data reading

## Metrics

### Revenue Metrics
- **Total Revenue**: Sum of all delivered order item prices
- **Revenue Growth Rate**: Year-over-year percentage change
- **Average Order Value (AOV)**: Average total value per order
- **Monthly Growth Trends**: Month-over-month performance

### Product Performance
- **Category Revenue**: Revenue by product category
- **Market Share**: Percentage of total revenue by category
- **Category Diversity**: Distribution across product lines

### Geographic Analysis
- **State Performance**: Revenue and order count by state
- **Market Penetration**: Number of active markets
- **Regional AOV**: Average order value by geographic region

### Customer Experience
- **Review Scores**: Average satisfaction rating (1-5 scale)
- **Satisfaction Distribution**: Percentage of high/low ratings
- **Delivery Performance**: Average delivery time and speed metrics

## Resources
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Claude Code Common Workflows](https://docs.anthropic.com/en/docs/claude-code/common-workflows)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Code Use Cases](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code)
- [Claude Code in Action - Anthropic Academy Course](https://anthropic.skilljar.com/claude-code-in-action)