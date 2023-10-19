import grpc
from app.models.iris import iris_pb2, iris_pb2_grpc
from app.models.penguins import penguins_pb2, penguins_pb2_grpc
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

HOST = "localhost"
IRIS_PORT = 8080
PENGUINS_PORT = 8088


iris_channel = grpc.insecure_channel("%s:%d" % (HOST, IRIS_PORT))
iris_stub = iris_pb2_grpc.IrisPredictorStub(iris_channel)

penguins_channel = grpc.insecure_channel("%s:%d" % (HOST, PENGUINS_PORT))
penguins_stub = penguins_pb2_grpc.PenguinsPredictorStub(penguins_channel)

router = APIRouter()


@router.get("/")
def read_root():
    """
    Returns welcoming message.

    Returns:
        str: "Welcome to service for classification of iris and penguins!"
    """
    return {"message": "Welcome to service for classification of iris and penguins!"}


@router.get("/iris/prediction")
def get_iris_prediction(
    sepal_length: float,
    sepal_width: float,
    petal_length: float,
    petal_width: float,
):
    """
    Get class prediction for iris sample.

    Args:
        sepal_length (float): length of sepal
        sepal_width (float): width of sepal
        petal_length (float): length of petal
        petal_width (float): width of petal

    Raises:
        HTTPException: if length or width of sepal or petal is not positive

    Returns:
        dict: JSON response including name of predicted class
    """
    if any(
        map(
            lambda x: True if x <= 0 else False,
            [sepal_length, sepal_width, petal_length, petal_width],
        )
    ):
        content = {"Error": "Length and width of sepal and petal must be positive"}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    request = iris_pb2.IrisPredictRequest(
        sepal_length=sepal_length,
        sepal_width=sepal_width,
        petal_length=petal_length,
        petal_width=petal_width,
    )
    response = iris_stub.PredictIrisSpecies(request)
    content = {"Predicted species": response.species}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.get("/penguins/prediction")
def get_penguins_prediction(
    island: str,
    bill_length_mm: float,
    bill_depth_mm: float,
    flipper_length_mm: int,
    body_mass_g: int,
    sex: str,
):
    """
    Get class prediction for penguins sample.

    Args:
        island (string): name of island
        bill_length_mm (float): length of bill in mm
        bill_depth_mm (float): depth of bill in mm
        flipper_length_mm (int): length of flipper in mm
        body_mass_g (int): mass of penguin body
        sex (string): sex of penguin

    Raises:
        HTTPException: if length or depth of bill, length of flipper, body mass is not positive or name of sex or island is incorrect

    Returns:
        dict: JSON response including name of predicted class
    """
    if any(
        map(
            lambda x: True if x <= 0 else False,
            [bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g],
        )
    ):
        content = {
            "Error": "Length and depth of bill, length of flipper, body mass must be positive"
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    islands = ["Torgersen", "Dream", "Biscoe"]
    if island not in islands:
        content = {"Error": f"Incorrect name of island. Choose from {islands}"}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    sexes = ["Male", "Female"]
    if sex not in sexes:
        content = {"Error": f"Incorrect name of sex. Choose from {sexes}"}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    request = penguins_pb2.PenguinsPredictRequest(
        island=island,
        bill_length_mm=bill_length_mm,
        bill_depth_mm=bill_depth_mm,
        flipper_length_mm=flipper_length_mm,
        body_mass_g=body_mass_g,
        sex=sex,
    )
    response = penguins_stub.PredictPenguinsSpecies(request)
    content = {"Predicted species": response.species}
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
