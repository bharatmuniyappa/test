{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "9567ff83",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "from datetime import datetime"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1f33e798",
   "metadata": {},
   "outputs": [],
   "source": [
    "!pip install streamlit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "d5ce1001",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:47:11.839 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:11.841 No runtime found, using MemoryCacheStorageManager\n",
      "2025-03-16 15:47:11.847 No runtime found, using MemoryCacheStorageManager\n",
      "2025-03-16 15:47:11.850 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:11.864 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:11.866 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:12.387 Thread 'Thread-8': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:12.408 Thread 'Thread-8': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:18.792 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:18.796 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# ---- Set page layout ----\n",
    "st.set_page_config(page_title=\"SuperStore KPI Dashboard\", layout=\"wide\")\n",
    "\n",
    "# ---- Load Data with Column Standardization ----\n",
    "@st.cache_data\n",
    "def load_data():\n",
    "    try:\n",
    "        df = pd.read_excel(\"Sample - Superstore.xlsx\", engine=\"openpyxl\")\n",
    "        df.columns = df.columns.str.strip().str.lower()  # Standardize column names\n",
    "        df[\"order date\"] = pd.to_datetime(df[\"order date\"], errors=\"coerce\")\n",
    "\n",
    "        if \"region\" not in df.columns:\n",
    "            st.error(f\"⚠️ 'Region' column not found! Available columns: {', '.join(df.columns)}\")\n",
    "            return pd.DataFrame()\n",
    "\n",
    "        return df\n",
    "    except FileNotFoundError:\n",
    "        st.error(\"⚠️ Dataset not found. Please upload 'Sample - Superstore.xlsx'.\")\n",
    "        return pd.DataFrame()\n",
    "\n",
    "df_original = load_data()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "251e8213",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:47:27.601 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:27.603 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:27.605 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:27.607 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:27.609 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:27.611 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:27.615 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:27.618 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator(_root_container=1, _parent=DeltaGenerator())"
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# ---- Debugging: Check Available Columns ----\n",
    "st.write(\"Available columns in dataset:\", df_original.columns.tolist())\n",
    "\n",
    "# ---- Sidebar Filters ----\n",
    "st.sidebar.title(\"Filters\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "90052d00",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Persistent Filter State\n",
    "def filter_selection(key, options):\n",
    "    if key not in st.session_state:\n",
    "        st.session_state[key] = \"All\"\n",
    "    return st.sidebar.selectbox(f\"Select {key}\", options=[\"All\"] + options, index=options.index(st.session_state[key]) if st.session_state[key] in options else 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "64de2626",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:47:48.937 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.939 Session state does not function when running a script without `streamlit run`\n",
      "2025-03-16 15:47:48.941 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.944 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.947 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.950 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.952 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.955 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.957 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.959 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:48.963 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# Region Filter (Using Lowercase Column Name)\n",
    "all_regions = sorted(df_original[\"region\"].dropna().unique())\n",
    "selected_region = filter_selection(\"Region\", all_regions)\n",
    "\n",
    "df_filtered = df_original if selected_region == \"All\" else df_original[df_original[\"region\"] == selected_region]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "b9278021",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:47:58.926 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.928 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.930 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.932 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.934 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.936 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.938 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.940 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.943 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:47:58.945 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# State Filter\n",
    "all_states = sorted(df_filtered[\"state\"].dropna().unique())\n",
    "selected_state = filter_selection(\"State\", all_states)\n",
    "\n",
    "df_filtered = df_filtered if selected_state == \"All\" else df_filtered[df_filtered[\"state\"] == selected_state]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "ccc21726",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:48:08.188 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.190 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.191 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.192 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.195 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.198 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.201 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.202 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.205 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:08.207 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# Category Filter\n",
    "all_categories = sorted(df_filtered[\"category\"].dropna().unique())\n",
    "selected_category = filter_selection(\"Category\", all_categories)\n",
    "\n",
    "df_filtered = df_filtered if selected_category == \"All\" else df_filtered[df_filtered[\"category\"] == selected_category]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "id": "70f3fab5",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:48:17.211 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.214 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.216 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.217 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.219 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.221 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.223 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.225 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.230 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:17.232 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# Sub-Category Filter\n",
    "all_subcats = sorted(df_filtered[\"sub-category\"].dropna().unique())\n",
    "selected_subcat = filter_selection(\"Sub-Category\", all_subcats)\n",
    "\n",
    "df_filtered = df_filtered if selected_subcat == \"All\" else df_filtered[df_filtered[\"sub-category\"] == selected_subcat]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "id": "b3f3157d",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:48:29.776 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.777 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.779 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.783 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.785 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.789 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.791 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.793 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.795 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:48:29.797 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# ---- Date Range Filter ----\n",
    "if df_filtered.empty:\n",
    "    min_date, max_date = df_original[\"order date\"].min(), df_original[\"order date\"].max()\n",
    "else:\n",
    "    min_date, max_date = df_filtered[\"order date\"].min(), df_filtered[\"order date\"].max()\n",
    "\n",
    "from_date = st.sidebar.date_input(\"From Date\", value=min_date, min_value=min_date, max_value=max_date)\n",
    "to_date = st.sidebar.date_input(\"To Date\", value=max_date, min_value=min_date, max_value=max_date)\n",
    "\n",
    "df_filtered = df_filtered[(df_filtered[\"order date\"] >= pd.to_datetime(from_date)) & (df_filtered[\"order date\"] <= pd.to_datetime(to_date))]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "9f9de8ac",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:49:06.827 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.828 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.832 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.834 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.842 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.844 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.847 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.849 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.850 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.852 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.855 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:06.857 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# ---- Title ----\n",
    "st.title(\"SuperStore KPI Dashboard\")\n",
    "\n",
    "# ---- KPI Section ----\n",
    "st.subheader(\"Key Performance Indicators\")\n",
    "total_sales = df_filtered[\"sales\"].sum() if not df_filtered.empty else 0\n",
    "total_quantity = df_filtered[\"quantity\"].sum() if not df_filtered.empty else 0\n",
    "total_profit = df_filtered[\"profit\"].sum() if not df_filtered.empty else 0\n",
    "margin_rate = (total_profit / total_sales) if total_sales != 0 else 0\n",
    "\n",
    "st.metric(\"Total Sales\", f\"${total_sales:,.2f}\")\n",
    "st.metric(\"Total Quantity Sold\", f\"{total_quantity:,}\")\n",
    "st.metric(\"Total Profit\", f\"${total_profit:,.2f}\")\n",
    "st.metric(\"Margin Rate\", f\"{margin_rate * 100:.2f}%\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "34f330b1",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:49:15.693 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:15.694 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:15.697 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:15.700 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:15.702 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:15.704 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:15.708 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:15.710 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# ---- KPI Selection ----\n",
    "st.subheader(\"Visualize KPI Trends & Insights\")\n",
    "kpi_options = [\"sales\", \"quantity\", \"profit\", \"margin rate\"]\n",
    "selected_kpi = st.radio(\"Select KPI to display:\", options=kpi_options, horizontal=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "299ae19b",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:49:21.061 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:21.063 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:21.064 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:21.934 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:21.936 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:21.938 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:21.940 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:22.138 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:22.140 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:22.142 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:22.144 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# ---- Visualizations ----\n",
    "if not df_filtered.empty:\n",
    "    daily_grouped = df_filtered.groupby(\"order date\").agg({\"sales\": \"sum\", \"quantity\": \"sum\", \"profit\": \"sum\"}).reset_index()\n",
    "    daily_grouped[\"margin rate\"] = daily_grouped[\"profit\"] / daily_grouped[\"sales\"].replace(0, 1)\n",
    "\n",
    "    product_grouped = df_filtered.groupby(\"product name\").agg({\"sales\": \"sum\", \"quantity\": \"sum\", \"profit\": \"sum\"}).reset_index()\n",
    "    product_grouped[\"margin rate\"] = product_grouped[\"profit\"] / product_grouped[\"sales\"].replace(0, 1)\n",
    "\n",
    "    product_grouped.sort_values(by=selected_kpi, ascending=False, inplace=True)\n",
    "    top_10 = product_grouped.head(10)\n",
    "\n",
    "    col1, col2 = st.columns(2)\n",
    "\n",
    "    with col1:\n",
    "        fig_line = px.line(daily_grouped, x=\"order date\", y=selected_kpi, title=f\"{selected_kpi} Over Time\", labels={\"order date\": \"Date\", selected_kpi: selected_kpi})\n",
    "        st.plotly_chart(fig_line, use_container_width=True)\n",
    "\n",
    "    with col2:\n",
    "        fig_bar = px.bar(top_10, x=selected_kpi, y=\"product name\", orientation=\"h\", title=f\"Top 10 Products by {selected_kpi}\")\n",
    "        st.plotly_chart(fig_bar, use_container_width=True)\n",
    "\n",
    "else:\n",
    "    st.warning(\"No data available for the selected filters and date range.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "id": "7050383f",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-03-16 15:49:48.646 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.648 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.650 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.652 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.652 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.652 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.660 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.952 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.952 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.952 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.952 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.952 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.965 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.967 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-03-16 15:49:48.970 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 47,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# ---- Additional Enhancements ----\n",
    "# Dark Mode Toggle\n",
    "dark_mode = st.sidebar.toggle(\"Dark Mode\")\n",
    "if dark_mode:\n",
    "    st.markdown(\"<style>body { background-color: #333333; color: white; }</style>\", unsafe_allow_html=True)\n",
    "else:\n",
    "    st.markdown(\"<style>body { background-color: white; color: black; }</style>\", unsafe_allow_html=True)\n",
    "\n",
    "# CSV Export\n",
    "csv = df_filtered.to_csv(index=False).encode(\"utf-8\")\n",
    "st.sidebar.download_button(\"Download Filtered Data\", csv, \"filtered_data.csv\", \"text/csv\")\n",
    "\n",
    "st.success(\"Dashboard loaded successfully!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5af17592",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
