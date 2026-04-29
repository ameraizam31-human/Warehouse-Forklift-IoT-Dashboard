# **Product Requirements Document (PRD): Warehouse Forklift Productivity Dashboard**

## **1\. Role & Context**

**Role:** Act as an expert Python Streamlit developer.

**Task:** Build a single-page Warehouse Forklift Productivity Dashboard using Streamlit and Pandas.

## **2\. Data Requirements (Dummy Data Generation)**

* **Timeframe:** Generate daily logs for 30 days for the month of April 2026 (April 1, 2026, to April 30, 2026).  
* **Workers:** Generate data for 5 named warehouse workers. The "Top 1" worker must be named "Ahmad". (You may assign realistic local names for the other 4, e.g., Muthu, Chong, Raju, Hafiz).  
* **Target Metrics (Strict):**  
  * For the top worker ("Ahmad"), the **total monthly sum** must be EXACTLY:  
    * 101 Unloaded IBC  
    * 305 Loaded IBC  
    * 50 Loading Pallet  
    * 15 Unloading Pallet  
    * 600 Standby IBC  
  * *Logic:* Distribute these exact numbers randomly but logically across the 30 days for Ahmad.  
  * For the remaining 4 workers, generate realistic random daily numbers, ensuring their overall monthly totals are slightly lower than Ahmad's totals.  
* **Data Caching (Crucial):** You MUST use the @st.cache\_data decorator for the pandas DataFrame generation function. This ensures the dummy data remains consistent across the session and does not randomly regenerate every time the user interacts with the UI filters.

## **3\. UI/UX & Interactivity Requirements**

* **Sidebar Filters:**  
  * Create a st.sidebar.  
  * Add a Date Range Picker (st.date\_input) covering the default range of April 1, 2026, to April 30, 2026\.  
* **Dynamic Behavior:** All charts, metrics, and tables in the main area must dynamically update based on the exact date range selected in the sidebar.

## **4\. Visualizations & Layout**

* **KPI Section:** \* Use st.metric (typically in st.columns) to display the filtered total numbers strictly for the Top 1 worker ("Ahmad").  
* **Charts:** \* Create a Stacked Bar Chart showing the breakdown of activities (Unloaded IBC, Loaded IBC, Loading Pallet, Unloading Pallet, Standby IBC) for **all 5 workers** within the selected date range.  
* **Raw Data:** \* Add a raw data table at the bottom of the page using st.dataframe for transparency, showing the filtered dataset based on the date range.

## **5\. Output Deliverables**

* Provide **only** the clean, well-commented, complete, and runnable app.py script. Do not provide unnecessary text outside the code block.