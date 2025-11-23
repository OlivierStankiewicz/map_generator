def surround_artifact_with_objects(artifact, object_type, count):
    """
    Surrounds the given artifact with a specified number of objects of a certain type.

    Parameters:
    artifact (Artifact): The artifact to be surrounded.
    object_type (str): The type of objects to surround the artifact with.
    count (int): The number of objects to place around the artifact.

    Returns:
    list: A list of objects placed around the artifact.
    """
    surrounding_objects = []
    for i in range(count):
        obj = create_object(object_type)
        position = calculate_position_around_artifact(artifact, i, count)
        obj.set_position(position)
        surrounding_objects.append(obj)
    
    return surrounding_objects