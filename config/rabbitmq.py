credentials = dict(
    host='localhost',
    user='guest',
    pwd='guest'
)

consumers = dict(
    parser=dict(
        exchange=dict(
            name='insider-exchange-parser',
            durable=True,
        ),
        queue=dict(
            name='insider-queue-parser',
            exclusive=False,
            durable=True,
        ),
        consumer=dict(
            autoAck=True,
        )
    )
)
