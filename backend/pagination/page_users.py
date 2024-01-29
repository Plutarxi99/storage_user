from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel
from typing_extensions import Self

from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams

# Класс для создания пагинации, который создает и возвращает pydantic class
class UserAPIParams(BaseModel, AbstractParams):
    page: int = Query(1, ge=1)
    size: int = Query(10, ge=1, le=100)

    def to_raw_params(self) -> RawParams:
        return RawParams(limit=self.size, offset=self.page)


class UserAPIPageInfoMeta(BaseModel):
    total: int
    page: int
    size: int


class UserAPIPageMeta(BaseModel):
    pagination: UserAPIPageInfoMeta


T = TypeVar("T")


class UserAPIPage(AbstractPage[T], Generic[T]):
    data: Sequence[T]
    meta: UserAPIPageMeta

    __params_type__ = UserAPIParams

    @classmethod
    def create(
            cls,
            items: Sequence[T],
            params: AbstractParams,
            *,
            total: Optional[int] = None,
            **kwargs: Any,
    ) -> Self:
        assert isinstance(params, UserAPIParams)
        assert total is not None

        return cls(
            data=items,
            meta={"pagination": {"total": total,
                                 "page": params.page,
                                 "size": params.size}},
            **kwargs,
        )
