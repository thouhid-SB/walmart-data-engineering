import great_expectations as gx


def get_gx_context():

    context = gx.get_context(mode="ephemeral")

    return context


def register_data_source(context):

    data_source = context.data_sources.add_pandas(
        name="pandas_source"
    )

    return data_source

def register_dataframe_asset(data_source, asset_name):

    data_asset = data_source.add_dataframe_asset(
        name=asset_name
    )

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        name=f"{asset_name}_batch"
    )

    return batch_definition

def validate_dataframe(
    context,
    data_source,
    df,
    asset_name,
    suite
) -> bool:

    # Register DataFrame asset
    batch_definition = register_dataframe_asset(
        data_source,
        asset_name
    )

    # Register expectation suite
    registered_suite = context.suites.add(suite)

    # Create validation definition
    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            name=f"{asset_name}_validation",
            data=batch_definition,
            suite=registered_suite
        )
    )

    # Execute validation
    result = validation_definition.run(
        batch_parameters={"dataframe": df}
    )

    # Display validation results
    print(f"\nValidating: {asset_name}")
    print("Validation successful:", result.success)

    for expectation_result in result.results:

        config = expectation_result.expectation_config

        if config is None:
            continue

        print(
            f"{config.type}: "
            f"{expectation_result.success}"
        )

    return result.success is True
