from typing import Union
from pydantic import BaseModel
from typing_extensions import List

# This is the base structure of response
# so if in the future we add a new endpoint, we can still use this model as its base.
# The model consists of response code and data.
# The response code in the body will help the client to verify whether the API call success or not.
class ResponseModel(BaseModel):
    response_code: int
    data: Union[dict, List[dict]] # make the response data flexible by allowing it to return dictionary or list of dictionary if in the future we add a new endpoint