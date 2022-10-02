import concurrent.futures as futures
import grpc
import grpc_reflection.v1alpha.reflection as grpc_reflection
import logging
import image_generic_pb2
import image_generic_pb2_grpc
import utils


class ServiceImpl(image_generic_pb2_grpc.ImageGenericServiceServicer):

    def __init__(self, calling_function):
        """
        Args:
            calling_function: the function that should be called
                              when a new request is received

                              the signature of the function should be:

                              (image: bytes) -> bytes

                              as described in the process method

        """
        self.__calling_fn = calling_function
        



    def process(self, request: image_generic_pb2.Image, context):
        """
        Image is the bytes of the image to process.

        Args:
            request: The ImageAndFeatures request to process
            context: Context of the gRPC call

        Returns:
            The Image with the applied function
        features={'kp','desc'}
        """
        image = request.data
        keypts, descriptors = self.__calling_fn(image)
        return image_generic_pb2.ImageAndFeatures(img=image_generic_pb2.Image(data=image),coords=keypts.tobytes(),descriptors=descriptors.tobytes(),numfeatures=keypts.shape[0])

    

if __name__ == '__main__':
    logging.basicConfig(
        format='[ %(levelname)s ] %(asctime)s (%(module)s) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

    calling_fn = utils.get_calling_function()
    if not calling_fn:
        exit(1)

    server = grpc.server(futures.ThreadPoolExecutor())
    image_generic_pb2_grpc.add_ImageGenericServiceServicer_to_server(
        ServiceImpl(calling_fn),
        server)

    # Add reflection
    service_names = (
        image_generic_pb2.DESCRIPTOR.services_by_name['ImageGenericService'].full_name,
        grpc_reflection.SERVICE_NAME
    )
    grpc_reflection.enable_server_reflection(service_names, server)

    utils.run_server(server)
