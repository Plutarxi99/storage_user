from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel
from typing_extensions import Self

from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams


class AdminAPIParams(BaseModel, AbstractParams):
    page: int = Query(1, ge=1)
    size: int = Query(10, ge=1, le=100)

    def to_raw_params(self) -> RawParams:
        return RawParams(limit=self.size, offset=self.page)


class AdminAPIPageInfoMeta(BaseModel):
    total: int
    page: int
    size: int


class AdminAPIPageMeta(BaseModel):
    pagination: AdminAPIPageInfoMeta


T = TypeVar("T")


class AdminAPIPage(AbstractPage[T], Generic[T]):
    data: Sequence[T]
    meta: AdminAPIPageMeta

    __params_type__ = AdminAPIParams

    @classmethod
    def create(
            cls,
            items: Sequence[T],
            params: AbstractParams,
            *,
            total: Optional[int] = None,
            **kwargs: Any,
    ) -> Self:
        assert isinstance(params, AdminAPIParams)
        assert total is not None

        return cls(
            data=items,
            meta={"pagination":
                {
                    "total": total,
                    "page": params.page,
                    "size": params.size
                }
            },
            **kwargs,
        )
