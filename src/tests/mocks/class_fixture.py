def patch_class_key(mocker, var: str, value):
    return mocker.patch(
        var,
        new_callable=mocker.PropertyMock,
        return_value=value,
    )
