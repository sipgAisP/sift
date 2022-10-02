# sift
AI4EU (acumos) component to compute sift features from images
This is a modification of the opencv component (https://github.com/DuarteMRAlves/opencv-grpc-service)

input: Image
output: Image and sift keypoints (coordinates and descriptor).

See test notebook for details (test_image_generic.ipynb in tests folder)

```shell
$ docker run --rm -it -p 8061:8061 -v pathtoexternal/externalfile.py=/workspace/external.py sipg/opencvsift:<specific tag>-latest
```
