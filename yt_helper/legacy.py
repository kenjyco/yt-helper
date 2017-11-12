try:
    import redis_helper as rh
    import input_helper as ih
    from redis import ConnectionError as RedisConnectionError

except ImportError:
    COMMENTS = None
else:
    try:
        COMMENTS = rh.Collection(
            'av',
            'comment',
            index_fields='basename',
            json_fields=','.join(ih.SPECIAL_TEXT_RETURN_FIELDS),
            insert_ts=True,
        )
    except RedisConnectionError:
        COMMENTS = None
