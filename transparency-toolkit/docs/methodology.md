# Methodology Overview

This document outlines the high-level approach for building a real-time
surveillance dashboard as described in the Public Health Transparency Toolkit.
Data ingestion routines gather weekly mortality and vaccination data. Processing
steps harmonize sources using DuckDB and Pandas/Polars. The analysis engine then
computes metrics such as age-stratified excess mortality ratios and
vaccination-mortality cross-correlations. The dashboard interface is implemented
using Streamlit with Altair/Vega visualizations.
