# insights_generator.py

import pandas as pd

def generate_insights(tracking_data, payouts):
    # Optional: Drop 'orders' from payouts to prevent '_x', '_y' confusion
    if 'orders' in payouts.columns:
        payouts = payouts.drop(columns=['orders'])

    # === Merge tracking and payouts data ===
    roas_df = tracking_data.merge(payouts, on='influencer_id', how='left')
    roas_df['total_payout'] = roas_df['total_payout'].fillna(1)
    roas_df['ROAS'] = (roas_df['revenue'] / roas_df['total_payout']).round(2)

    # === Basic KPIs ===
    total_revenue = roas_df['revenue'].sum()
    total_orders = roas_df['orders'].sum()
    aov = round(total_revenue / total_orders, 2) if total_orders else 0

    # === Campaign-based aggregation ===
    revenue_by_campaign = roas_df.groupby('campaign')['revenue'].sum().sort_values(ascending=False)
    # Change orders_by_date line
    orders_by_date = tracking_data.copy()
    orders_by_date['date'] = pd.to_datetime(orders_by_date['date'])
    orders_by_date = orders_by_date.set_index('date').resample('D')['orders'].sum()


    # === ROAS Table ===
    roas_table = roas_df[['campaign', 'influencer_id', 'revenue', 'total_payout', 'ROAS']]

    # === Top Influencers ===
    top_influencers = roas_df.groupby('influencer_id').agg({
        'revenue': 'sum',
        'ROAS': 'mean'
    }).sort_values(by='revenue', ascending=False).head(5).reset_index()

    # === Payout Efficiency ===
    payout_efficiency = roas_df.groupby('influencer_id').agg({
        'revenue': 'sum',
        'orders': 'sum',
        'total_payout': 'mean',
        'ROAS': 'mean'
    }).reset_index()

    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'aov': aov,
        'revenue_by_campaign': revenue_by_campaign,
        'orders_by_date': orders_by_date,
        'roas_table': roas_table,
        'top_influencers': top_influencers,
        'payout_efficiency': payout_efficiency
    }
