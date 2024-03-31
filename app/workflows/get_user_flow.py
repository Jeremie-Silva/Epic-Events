from prefect import flow


@flow
def get_user_flow():
    return {"user": "test_flow_get_user"}
