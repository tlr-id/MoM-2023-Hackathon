METADATA_FIELDS= [
    #'id', 
    #'name', 
    #'created_at', 
    'code2', 
    #'band', 
    #'pronoun_title', # could be nice
    #'gender_title', # could be nice
    #'gender', # could be nice
    #'isni', 
    #'cover_url', 
    #'hometown_city', # could be nice
    #'current_city', # could be nice# could be nice
    #'current_city_id', # could be nice
    #'band_members', 
    'booking_agent', 
    'record_label', 
    'press_contact', 
    'general_manager', 
    #'description', 
    #'is_custom_description', 
    'cm_artist_rank', 
    'cm_artist_score', 
    'rank_eg', 
    'rank_fb', 
    'image_url', 
    #'topSongwriterCollaborators', 
    #'tags', 
    #'genres', # could be nice
    #'topSongwriterId', 
    'career_status', 
    'cm_statistics',
    ]

FAN_METRICS = [
    {"spotify": ["followers", "popularity", "listeners"]},
    {"deezer": ["fans"]},
    {"facebook": ["likes", "talks"]},
    {"youtube_artist": ["daily_views", "monthly_views"]},
    {"instagram": ["followers"]},
    {"bandsintown": ["followers"]},
    {"soundcloud": ["followers"]},
    {"tiktok": ["followers", "likes"]},
]

INSTAGRAM_FIELDS = [
    "top_countries", 
    #"top_cities", 
    "audience_genders_per_age", 
    #"audience_ethnicities", 
    #"audience_genders", 
    "audience_brand_affinities", 
    "audience_interests", 
    "followers", 
    "avg_likes_per_post", 
    "avg_commments_per_post", 
    "engagement_rate", 
    #"notable_followers",
]

YOUTUBE_FIELDS = [
    "top_countries",
    #"audience_genders_per_age", # doesnt work with geoOnly
    #"audience_genders",# doesnt work with geoOnly
    #"notable_subscribers",
    #"timestp",
    "subscribers",
    "avg_likes_per_post",
    "avg_commments_per_post",
    "engagement_rate",
]

TIKTOK_FIELDS = [
    "top_countries",
    "audience_genders_per_age",
    "audience_genders",
    #"notable_followers",
    "followers",
    "avg_likes_per_post",
    "avg_commments_per_post",
    "engagement_rate",
]