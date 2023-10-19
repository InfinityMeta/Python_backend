import time
from concurrent import futures

import app.models.iris.iris_pb2 as iris_pb2
import app.models.iris.iris_pb2_grpc as iris_pb2_grpc
import app.models.penguins.penguins_pb2 as penguins_pb2
import app.models.penguins.penguins_pb2_grpc as penguins_pb2_grpc
import grpc
import joblib

HOUR_IN_SECONDS = 60 * 24
IRIS_PORT = 8080
PENGUINS_PORT = 8088
MAX_WORKERS = 10

IRIS_PATH = "app/models/iris/iris_model.pickle"
PENGUINS_PATH = "app/models/penguins/penguins_model.pickle"


class IrisPredictor(iris_pb2_grpc.IrisPredictorServicer):
    model = None

    @classmethod
    def get_or_create_model(cls):
        """
        Get or create iris classification model
        """
        if cls.model is None:
            path = IRIS_PATH
            cls.model = joblib.load(path)
        return cls.model

    def PredictIrisSpecies(self, request, context):
        """
        Get prediction for iris sample
        """
        model = self.__class__.get_or_create_model()
        iris = {0: "Iris-setosa", 1: "Iris-versicolor", 2: "Iris-virginica"}

        sepal_length = request.sepal_length
        sepal_width = request.sepal_width
        petal_length = request.petal_length
        petal_width = request.petal_width
        result = model.predict([[sepal_length, sepal_width, petal_length, petal_width]])
        return iris_pb2.IrisPredictReply(species=iris[result[0]])


class PenguinsPredictor(penguins_pb2_grpc.PenguinsPredictorServicer):
    model = None

    @classmethod
    def get_or_create_model(cls):
        """
        Get or create penguins classification model.
        """
        if cls.model is None:
            path = PENGUINS_PATH
            cls.model = joblib.load(path)
        return cls.model

    def PredictPenguinsSpecies(self, request, context):
        """
        Get prediction for penguins sample
        """
        model = self.__class__.get_or_create_model()
        penguins = {0: "Adelie", 1: "Chinstrap", 2: "Gentoo"}

        Biscoe = 1 if request.island == "Biscoe" else 0
        Dream = 1 if request.island == "Dream" else 0
        Torgersen = 1 if request.island == "Torgersen" else 0
        bill_length_mm = request.bill_length_mm
        bill_depth_mm = request.bill_depth_mm
        flipper_length_mm = request.flipper_length_mm
        body_mass_g = request.body_mass_g
        sex = 0 if request.sex == "Male" else 1
        result = model.predict(
            [
                [
                    bill_length_mm,
                    bill_depth_mm,
                    flipper_length_mm,
                    body_mass_g,
                    sex,
                    Biscoe,
                    Dream,
                    Torgersen,
                ]
            ]
        )
        return penguins_pb2.PenguinsPredictReply(species=penguins[result[0]])


def serve(iris_port, penguins_port, max_workers):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    iris_pb2_grpc.add_IrisPredictorServicer_to_server(IrisPredictor(), server)
    penguins_pb2_grpc.add_PenguinsPredictorServicer_to_server(
        PenguinsPredictor(), server
    )
    server.add_insecure_port("[::]:{iris_port}".format(iris_port=iris_port))
    server.add_insecure_port("[::]:{penguins_port}".format(penguins_port=penguins_port))
    server.start()
    try:
        while True:
            time.sleep(HOUR_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve(
        iris_port=IRIS_PORT,
        penguins_port=PENGUINS_PORT,
        max_workers=MAX_WORKERS,
    )
