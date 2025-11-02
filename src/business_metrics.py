"""
Business metrics calculation module for e-commerce data analysis.

This module provides classes and functions for calculating various business
performance metrics from e-commerce sales data. It focuses purely on calculations
and does not include visualization code.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


class BusinessMetricsCalculator:
    """
    A class for calculating various business metrics from e-commerce data.

    This class provides methods to calculate revenue metrics, product performance,
    geographic analysis, customer satisfaction, and delivery performance.

    Attributes:
        sales_data (pd.DataFrame): Processed sales dataset
    """

    def __init__(self, sales_data: pd.DataFrame):
        """
        Initialize the metrics calculator.

        Args:
            sales_data (pd.DataFrame): Processed sales dataset containing all necessary
                                     columns for analysis
        """
        self.sales_data = sales_data.copy()
        self._validate_data()

    def _validate_data(self):
        """
        Validate that required columns exist in the data.

        Raises:
            ValueError: If required columns are missing
        """
        required_cols = ['price', 'order_id', 'purchase_year']
        missing_cols = [col for col in required_cols if col not in self.sales_data.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

    def calculate_revenue_metrics(self,
                                 current_year: int,
                                 previous_year: Optional[int] = None) -> Dict[str, float]:
        """
        Calculate revenue-related metrics for a given year.

        Calculates:
        - Total revenue: Sum of all item prices
        - Total orders: Count of unique orders
        - Average order value (AOV): Average total value per order
        - Total items sold: Count of line items
        - Growth metrics (if previous year provided): Revenue, order, and AOV growth rates

        Args:
            current_year (int): Year to analyze
            previous_year (int, optional): Comparison year for growth calculations

        Returns:
            Dict[str, float]: Revenue metrics including totals and growth rates
        """
        current_data = self.sales_data[self.sales_data['purchase_year'] == current_year]

        metrics = {
            'total_revenue': current_data['price'].sum(),
            'total_orders': current_data['order_id'].nunique(),
            'average_order_value': current_data.groupby('order_id')['price'].sum().mean(),
            'total_items_sold': len(current_data)
        }

        # Calculate growth metrics if comparison year is provided
        if previous_year:
            previous_data = self.sales_data[self.sales_data['purchase_year'] == previous_year]
            prev_revenue = previous_data['price'].sum()
            prev_orders = previous_data['order_id'].nunique()
            prev_aov = previous_data.groupby('order_id')['price'].sum().mean()

            metrics.update({
                'revenue_growth_rate': ((metrics['total_revenue'] - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0,
                'order_growth_rate': ((metrics['total_orders'] - prev_orders) / prev_orders * 100) if prev_orders > 0 else 0,
                'aov_growth_rate': ((metrics['average_order_value'] - prev_aov) / prev_aov * 100) if prev_aov > 0 else 0,
                'previous_year_revenue': prev_revenue,
                'previous_year_orders': prev_orders,
                'previous_year_aov': prev_aov
            })

        return metrics

    def calculate_monthly_trends(self, year: int) -> pd.DataFrame:
        """
        Calculate month-over-month trends for a given year.

        Calculates monthly:
        - Total revenue
        - Total orders
        - Average order value
        - Growth rates for each metric

        Args:
            year (int): Year to analyze

        Returns:
            pd.DataFrame: Monthly trends with revenue, orders, AOV, and growth rates
        """
        year_data = self.sales_data[self.sales_data['purchase_year'] == year]

        # Aggregate monthly metrics
        monthly_metrics = year_data.groupby('purchase_month').agg({
            'price': 'sum',
            'order_id': 'nunique'
        }).reset_index()

        monthly_metrics.columns = ['month', 'revenue', 'orders']

        # Calculate average order value for each month
        monthly_metrics['avg_order_value'] = year_data.groupby('purchase_month').apply(
            lambda x: x.groupby('order_id')['price'].sum().mean()
        ).values

        # Calculate month-over-month growth rates
        monthly_metrics['revenue_growth'] = monthly_metrics['revenue'].pct_change() * 100
        monthly_metrics['order_growth'] = monthly_metrics['orders'].pct_change() * 100
        monthly_metrics['aov_growth'] = monthly_metrics['avg_order_value'].pct_change() * 100

        return monthly_metrics

    def analyze_product_performance(self, year: int, top_n: int = 10) -> Dict[str, pd.DataFrame]:
        """
        Analyze product category performance for a given year.

        Calculates category-level:
        - Total revenue
        - Average item price
        - Number of items sold
        - Number of unique orders
        - Revenue share percentage

        Args:
            year (int): Year to analyze
            top_n (int): Number of top categories to return in top_categories. Defaults to 10.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing:
                - 'all_categories': All categories sorted by revenue
                - 'top_categories': Top N categories by revenue
                Or {'error': message} if product data not available
        """
        year_data = self.sales_data[self.sales_data['purchase_year'] == year]

        if 'product_category_name' not in year_data.columns:
            return {'error': 'Product category data not available'}

        # Aggregate category metrics
        category_metrics = year_data.groupby('product_category_name').agg({
            'price': ['sum', 'mean', 'count'],
            'order_id': 'nunique'
        }).round(2)

        category_metrics.columns = ['total_revenue', 'avg_item_price', 'items_sold', 'unique_orders']
        category_metrics = category_metrics.reset_index()

        # Calculate revenue share percentage
        category_metrics['revenue_share'] = (
            category_metrics['total_revenue'] / category_metrics['total_revenue'].sum() * 100
        ).round(2)

        # Sort by revenue descending
        category_metrics = category_metrics.sort_values('total_revenue', ascending=False)

        return {
            'all_categories': category_metrics,
            'top_categories': category_metrics.head(top_n)
        }

    def analyze_geographic_performance(self, year: int) -> pd.DataFrame:
        """
        Analyze sales performance by geographic region (state).

        Calculates state-level:
        - Total revenue
        - Total orders
        - Average order value

        Args:
            year (int): Year to analyze

        Returns:
            pd.DataFrame: Geographic performance metrics sorted by revenue descending
                        Or DataFrame with error message if data not available
        """
        year_data = self.sales_data[self.sales_data['purchase_year'] == year]

        if 'customer_state' not in year_data.columns:
            return pd.DataFrame({'error': ['Geographic data not available']})

        # Aggregate state-level metrics
        state_metrics = year_data.groupby('customer_state').agg({
            'price': 'sum',
            'order_id': 'nunique'
        }).reset_index()

        state_metrics.columns = ['state', 'revenue', 'orders']

        # Calculate average order value by state
        state_metrics['avg_order_value'] = year_data.groupby('customer_state').apply(
            lambda x: x.groupby('order_id')['price'].sum().mean()
        ).values

        # Sort by revenue descending
        state_metrics = state_metrics.sort_values('revenue', ascending=False)

        return state_metrics

    def analyze_customer_satisfaction(self, year: int) -> Dict[str, float]:
        """
        Calculate customer satisfaction metrics based on review scores.

        Calculates:
        - Average review score (1-5 scale)
        - Total number of reviews
        - Percentage of 5-star reviews
        - Percentage of 4+ star reviews (high satisfaction)
        - Percentage of 1-2 star reviews (low satisfaction)

        Note: Metrics are calculated at order level (duplicates removed) to avoid
        inflating counts since reviews are per order, not per line item.

        Args:
            year (int): Year to analyze

        Returns:
            Dict[str, float]: Customer satisfaction metrics
                            Or {'error': message} if review data not available
        """
        year_data = self.sales_data[self.sales_data['purchase_year'] == year]

        if 'review_score' not in year_data.columns:
            return {'error': 'Review data not available'}

        # Remove duplicates to analyze at order level (not item level)
        order_data = year_data.drop_duplicates('order_id')

        metrics = {
            'avg_review_score': order_data['review_score'].mean(),
            'total_reviews': order_data['review_score'].count(),
            'score_5_percentage': (order_data['review_score'] == 5).mean() * 100,
            'score_4_plus_percentage': (order_data['review_score'] >= 4).mean() * 100,
            'score_1_2_percentage': (order_data['review_score'] <= 2).mean() * 100
        }

        return metrics

    def analyze_delivery_performance(self, year: int) -> Dict[str, float]:
        """
        Calculate delivery performance metrics.

        Calculates:
        - Average delivery time in days
        - Median delivery time in days
        - Percentage of fast deliveries (3 days or less)
        - Percentage of slow deliveries (more than 7 days)

        Note: Metrics are calculated at order level (duplicates removed) and
        exclude orders with missing delivery dates.

        Args:
            year (int): Year to analyze

        Returns:
            Dict[str, float]: Delivery performance metrics
                            Or {'error': message} if delivery data not available
        """
        year_data = self.sales_data[self.sales_data['purchase_year'] == year]

        if 'delivery_days' not in year_data.columns:
            return {'error': 'Delivery data not available'}

        # Remove duplicates for order-level analysis and drop missing values
        order_data = year_data.drop_duplicates('order_id')
        order_data = order_data.dropna(subset=['delivery_days'])

        metrics = {
            'avg_delivery_days': order_data['delivery_days'].mean(),
            'median_delivery_days': order_data['delivery_days'].median(),
            'fast_delivery_percentage': (order_data['delivery_days'] <= 3).mean() * 100,
            'slow_delivery_percentage': (order_data['delivery_days'] > 7).mean() * 100
        }

        return metrics

    def generate_comprehensive_report(self,
                                    current_year: int,
                                    previous_year: Optional[int] = None) -> Dict[str, any]:
        """
        Generate a comprehensive business metrics report.

        Combines all metric categories into a single report including:
        - Revenue metrics with year-over-year comparisons
        - Monthly trends
        - Product category performance
        - Geographic performance
        - Customer satisfaction metrics
        - Delivery performance metrics

        Args:
            current_year (int): Year to analyze
            previous_year (int, optional): Comparison year for growth calculations

        Returns:
            Dict[str, any]: Comprehensive metrics report containing all analysis results
        """
        report = {
            'analysis_period': current_year,
            'comparison_period': previous_year,
            'revenue_metrics': self.calculate_revenue_metrics(current_year, previous_year),
            'monthly_trends': self.calculate_monthly_trends(current_year),
            'product_performance': self.analyze_product_performance(current_year),
            'geographic_performance': self.analyze_geographic_performance(current_year),
            'customer_satisfaction': self.analyze_customer_satisfaction(current_year),
            'delivery_performance': self.analyze_delivery_performance(current_year)
        }

        return report


def format_currency(value: float) -> str:
    """
    Format a numeric value as currency.

    Args:
        value (float): Numeric value to format

    Returns:
        str: Formatted currency string (e.g., "$1,234.56")
    """
    return f"${value:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a numeric value as percentage.

    Args:
        value (float): Numeric value to format
        decimals (int): Number of decimal places. Defaults to 1.

    Returns:
        str: Formatted percentage string (e.g., "25.5%")
    """
    return f"{value:.{decimals}f}%"


def print_metrics_summary(report: Dict[str, any]) -> None:
    """
    Print a formatted summary of business metrics to console.

    This function provides a quick overview of key business metrics
    in a readable format.

    Args:
        report (Dict): Business metrics report from generate_comprehensive_report()
    """
    print("=" * 60)
    print(f"BUSINESS METRICS SUMMARY - {report['analysis_period']}")
    print("=" * 60)

    # Revenue metrics
    revenue_metrics = report['revenue_metrics']
    print(f"\nREVENUE PERFORMANCE:")
    print(f"  Total Revenue: {format_currency(revenue_metrics['total_revenue'])}")
    print(f"  Total Orders: {revenue_metrics['total_orders']:,}")
    print(f"  Average Order Value: {format_currency(revenue_metrics['average_order_value'])}")

    if 'revenue_growth_rate' in revenue_metrics:
        print(f"  Revenue Growth: {format_percentage(revenue_metrics['revenue_growth_rate'])}")
        print(f"  Order Growth: {format_percentage(revenue_metrics['order_growth_rate'])}")

    # Customer satisfaction
    if 'error' not in report['customer_satisfaction']:
        satisfaction = report['customer_satisfaction']
        print(f"\nCUSTOMER SATISFACTION:")
        print(f"  Average Review Score: {satisfaction['avg_review_score']:.2f}/5.0")
        print(f"  High Satisfaction (4+): {format_percentage(satisfaction['score_4_plus_percentage'])}")

    # Delivery performance
    if 'error' not in report['delivery_performance']:
        delivery = report['delivery_performance']
        print(f"\nDELIVERY PERFORMANCE:")
        print(f"  Average Delivery Time: {delivery['avg_delivery_days']:.1f} days")
        print(f"  Fast Delivery (<=3 days): {format_percentage(delivery['fast_delivery_percentage'])}")

    print("=" * 60)
