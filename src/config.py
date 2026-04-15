SELECTED_FEATURES = [
    'duration','protocol_type','service','flag',
    'src_bytes','dst_bytes','logged_in','num_failed_logins',
    'count','srv_count','serror_rate','rerror_rate',
    'num_compromised','num_root','num_file_creations',
    'num_shells','num_access_files','hot'
]

CATEGORICAL_COLUMNS = ['protocol_type', 'service', 'flag']