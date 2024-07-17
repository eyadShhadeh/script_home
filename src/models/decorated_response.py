from typing import Dict, Generic, Optional, Tuple, TypeVar


DataT = TypeVar('DataT')


class APIResponse(Generic[DataT]):
    """
        A generic response model
    """
    success: bool = True
    metadata: Optional[Dict[str, str]] = None
    errors: Optional[Tuple[str, ...]] = None
    debug: Optional[Tuple[str, ...]] = None
    results: Optional[DataT] = None
