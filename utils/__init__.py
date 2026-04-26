"""
Data Science Project Utilities

This package contains utility functions for common data science tasks and journalism workflows.
"""

from .data_utils import (
    quick_info,
    plot_distributions,
    correlation_analysis,
    detect_outliers,
    clean_column_names,
    memory_optimization,
    create_date_features,
    categorical_analysis
)

from .journalism_utils import (
    quick_export_for_web,
    create_story_charts,
    data_fact_check,
    quick_summary_table,
    compare_periods
)

from .memory_utils import (
    show_process_memory,
    dataframe_memory_mb
)

__all__ = [
    # Data analysis utilities
    'quick_info',
    'plot_distributions',
    'correlation_analysis',
    'detect_outliers',
    'clean_column_names',
    'memory_optimization',
    'create_date_features',
    'categorical_analysis',
    
    # Journalism utilities
    'quick_export_for_web',
    'create_story_charts',
    'data_fact_check',
    'quick_summary_table',
    'compare_periods',
    'show_process_memory',
    'dataframe_memory_mb'
]
