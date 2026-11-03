def transfer_to_team(category):
    cat_map_team={
        'feature_request': 'product_team',
        'billing_cancellation': 'billing_team',
        'data_privacy': 'compliance_team',
        'account_access': 'auth_team',
        'technical_issue': 'engineering',
        "complaint_and_query": 'success_team'
    }
    return cat_map_team.get(category, 'support_team') 