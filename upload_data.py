import roboflow

rf = roboflow.Roboflow(api_key='rf9QkLi7Bku988P9f2lH')

# get a workspace
workspace = rf.workspace('fire-fc9mg')
# print(workspace)
# Upload data set to a new/existing project
workspace.upload_dataset(
    r"E:\CapstoneB\new_dataset\tempo\tempo2.0",     # This is your dataset path
    "preview_data",   # This will either create or get a dataset with the given ID
    num_workers=10,
    project_license="MIT",
    project_type="object-detection",
    batch_name=None,
    num_retries=0
)

